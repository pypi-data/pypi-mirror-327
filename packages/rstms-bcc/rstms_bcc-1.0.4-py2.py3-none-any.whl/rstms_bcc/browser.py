# baikal controller browser puppeteer

import logging
import os
from pathlib import Path
from pprint import pformat
from typing import Any, Dict, List, Tuple

import arrow
from bs4 import BeautifulSoup
from pydantic import validate_call
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait

from . import settings
from .firefox_profile import Profile
from .models import (
    VALID_TOKEN_CHARS,
    Account,
    AddBookRequest,
    AddUserRequest,
    Book,
    DeleteBookRequest,
    DeleteUserRequest,
    User,
)
from .passwd import Accounts
from .version import __version__

LOG_SOUP = False
POST_DELETE_TIMEOUT = 5


class BrowserException(Exception):
    pass


class BrowserInterfaceFailure(BrowserException):
    pass


class InitFailed(BrowserException):
    pass


class AddFailed(BrowserException):
    pass


class DeleteFailed(BrowserException):
    pass


class UnexpectedServerResponse(BrowserException):
    pass


class Session:

    def __init__(self):

        self.logger = logging.getLogger(settings.LOGGER_NAME)
        self.logger.setLevel(settings.LOG_LEVEL)

        self.logger.info("Browser session startup")
        self.driver = None
        self.logged_in = False
        self.startup_time = arrow.now()
        self.reset_time = None

        self.profile = Profile()
        self.profile.AddCert(settings.CLIENT_CERT, settings.CLIENT_KEY)
        if settings.FIREFOX_BIN:
            self.logger.info(f"browser binary: {settings.FIREFOX_BIN}")
        if settings.WEBDRIVER_BIN:
            self.logger.info(f"webdriver binary: {settings.WEBDRIVER_BIN}")
        if settings.HEADLESS:
            self.logger.info("(headless mode)")

    def _load_driver(self):

        if not self.driver:
            options = webdriver.FirefoxOptions()
            if settings.FIREFOX_BIN:
                options.binary_location = settings.FIREFOX_BIN
                bindir = Path(settings.FIREFOX_BIN).parent
                # ensure browser binary is on PATH
                if str(bindir) not in os.environ["PATH"].split(":"):
                    os.environ["PATH"] = str(bindir) + ":" + os.environ["PATH"]
            if settings.HEADLESS:
                options.add_argument("--headless")
            options.profile = webdriver.FirefoxProfile(settings.PROFILE_DIR)
            options.profile.set_preference("security.default_personal_cert", "Select Automatically")
            kwargs = {}
            if settings.WEBDRIVER_BIN:
                kwargs["executable_path"] = settings.WEBDRIVER_BIN
            service = webdriver.FirefoxService(**kwargs)
            self.driver = webdriver.Firefox(options=options, service=service)
            self.logger.debug(pformat(self.driver.capabilities))

    def shutdown(self):
        self.logger.debug("request: shutdown")
        if self.logged_in:
            self.logout()
        if self.driver:
            self.driver.quit()
            self.driver = None
        self.logger.debug("shutdown: complete")

    @validate_call
    def _find_elements(
        self,
        name: str,
        selector: str,
        *,
        parent: Any | None = None,
        with_text: str | None = None,
        allow_none: bool | None = False,
        click: bool | None = False,
    ) -> List[Any]:
        if parent is None:
            parent = self.driver
        try:
            elements = parent.find_elements(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            if allow_none:
                return []
            raise BrowserInterfaceFailure(f"{name} not found: {selector=} {with_text=}")

        if elements is not None:
            if with_text:
                elements = [element for element in elements if element.text == with_text]
            if elements:
                if click:
                    elements[0].click()
                return elements
            if allow_none:
                return elements
        raise BrowserInterfaceFailure(f"{name} not found: {selector=} {with_text=}")

    @validate_call
    def _find_element(
        self,
        name: str,
        selector: str,
        *,
        parent: Any | None = None,
        with_text: str | None = None,
        with_classes: List[str] | None = [],
    ) -> Any:
        if parent is None:
            parent = self.driver
        try:
            element = parent.find_element(By.CSS_SELECTOR, selector)
        except NoSuchElementException:
            raise BrowserInterfaceFailure(f"{name} not found: {selector=} {with_text=}")

        if element:
            if with_text:
                if element.text != with_text:
                    raise BrowserInterfaceFailure(f"{name} text mismatch: expected='{with_text}' got='{element.text}'")
            if with_classes:
                classes = element.get_attribute("class").split(" ")
                for cls in with_classes:
                    if cls not in classes:
                        raise BrowserInterfaceFailure(
                            f"{name} expected class not found: expected={cls} classes={classes} {selector=}"
                        )
            return element
        raise BrowserInterfaceFailure(f"{name} element not found: {selector=}")

    @validate_call
    def _click_button(self, name: str, selector: str, *, parent: Any | None = None, with_text: str | None = None):
        if with_text is not None:
            self._find_elements(name, selector, parent=parent, with_text=with_text, click=True)
        else:
            self._find_element(name, selector, parent=parent, with_text=with_text).click()

    @validate_call
    def _check_popups(self, require_none: bool | None = False) -> List[str]:
        messages = self._find_elements("popup messages", 'html > body [id="message"]', allow_none=True)
        ret = [message.text for message in messages]
        if ret and require_none:
            raise UnexpectedServerResponse("\n".join(ret).replace("\n", ": "))
        return ret

    @validate_call
    def _set_text(self, name: str, selector: str, text: str | None):
        element = self._find_element(name, selector)
        element.clear()
        if text:
            element.send_keys(text)

    @validate_call
    def _get(self, path: str):
        self._load_driver()
        url = settings.CALDAV_URL + path
        self.logger.debug(f"GET {url}")
        try:
            self.driver.get(url)
        except WebDriverException as ex:
            raise BrowserInterfaceFailure(ex.msg)

        if LOG_SOUP:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            source = soup.prettify()
            for line in source.split("\n"):
                self.logger.debug(line)

    @validate_call
    def login(self, admin: Account):
        self.logger.debug("request: login")
        if self.logged_in == admin.username:
            self.logger.debug(f"login: already logged in as {admin.username}")
            return

        self._get("/admin/")

        if self.driver.title == "Baïkal Maintainance":
            raise BrowserInterfaceFailure("server not initialized")

        self.logger.debug(f"connected: {self.driver.title}")

        self._set_text("login username field", 'body form input[id="login"]', admin.username)
        self._set_text("login password field", 'body form input[id="password"]', admin.password)
        self._click_button("login authenticate button", "body form button", with_text="Authenticate")
        self._check_popups(require_none=True)
        self.logged_in = admin.username
        self.logger.debug(f"login: authenticated as {admin.username}")

    @validate_call
    def initialize(self, admin: Account) -> Dict[str, str]:
        self.logger.debug("request: initialize")

        self._get("/admin/install/")
        if self.driver.title == "" and "Installation was already completed." in self.driver.page_source:
            raise InitFailed("initialize: already initialized")

        if self.driver.title != "Baïkal Maintainance":
            raise BrowserInterfaceFailure(f"unexpected page title: {self.driver.title}")

        self.logger.info(f"Initialize: {self.driver.title}")

        # TODO: support parameters for configuration options

        while True:
            if self._find_elements(
                "start button",
                "body .btn-success",
                with_text="Start using Baïkal",
                allow_none=True,
                click=True,
            ):
                if self.driver.current_url.endswith("/baikal/admin/"):
                    self.logger.info("initialize: successfully configured")
                    return dict(message="initialized")
                else:
                    raise InitFailed("unexpected url after start button: {self.driver.current_url}")
            jumbotron = self._find_element("initialization title", "body .jumbotron")
            title_text = jumbotron.text.lower()
            if "database setup" in title_text:
                self.logger.info("initialize: confirming default database config")
                self._click_button("database init save changes button", "body form .btn", with_text="Save changes")
            elif "initialization wizard" in title_text:
                self.logger.info("initialize: setting timezone")
                timezone = self._find_element("init timezone selector", 'body form select[name="data[timezone]"]')
                select = Select(timezone)
                select.select_by_visible_text("UTC")
                self.logger.info("initialize: clearing invite address")
                self._set_text("init invite address", 'body form input[name="data[invite_from]"]', None)
                self.logger.info("initialize: setting admin password")
                self._set_text(
                    "init admin password",
                    'body form input[name="data[admin_passwordhash]"]',
                    admin.password,
                )
                self._set_text(
                    "init admin password confirmation",
                    'body form input[name="data[admin_passwordhash_confirm]"]',
                    admin.password,
                )
                self._click_button("general init save changes button", "body form .btn", with_text="Save changes")
            else:
                raise InitFailed(f"unexpected init title: {jumbotron.text}")

        raise BrowserInterfaceFailure("initialization failed")

    def logout(self):
        self.logger.debug("request: logout")
        if self.logged_in:
            links = self._navbar_links()
            if "Logout" in links:
                links["Logout"].click()
            else:
                self.logger.warning("logout: navbar link not present, trying GET refresh")
                self._get("/admin/")
                self._click_navbar_link("logout", "Logout")
            self.logged_in = False
            links = self._navbar_links().keys()
            if list(links) != ["Web Admin"]:
                raise BrowserInterfaceFailure(f"logout: unexpected navbar content after logout: {links}")
            self.logger.debug("logout: logged out")
        else:
            self.logger.debug("logout: not logged in")

    @validate_call
    def _navbar_links(self):
        navbars = self._find_elements("navbar", "div.navbar")
        if len(navbars) != 1:
            raise BrowserInterfaceFailure("multiple navbars located")
        links = {e.text: e for e in self._find_elements("navbar links", "a", parent=navbars[0]) if e.text}
        return links

    @validate_call
    def _click_navbar_link(self, name: str, label: str):
        links = self._navbar_links()
        link = links.get(label, None)
        if label not in links:
            raise BrowserInterfaceFailure(f"{name}: navbar link {label} not found in: {list(links.keys())}")
        link.click()

    @validate_call
    def _table_rows(self, name: str, allow_none: bool | None = True):
        rows = self._find_elements(f"{name} table body rows", "body table tbody tr", allow_none=True)
        if not rows:
            message = f"no {name} table body rows found"
            if allow_none:
                self.logger.warning(message)
            else:
                raise BrowserInterfaceFailure(message)
        return rows

    @validate_call
    def _parse_user_row(self, row: Any) -> Dict[str, str]:
        col_username = self._find_element("user table row displayname column", "td.col-username", parent=row)
        username, _, tail = col_username.text.partition("\n")
        displayname, _, email = tail.partition(" <")
        email = email.strip(">")
        ret = self._parse_row_info("user", row)
        ret.update(dict(username=username, displayname=displayname, email=email))
        return ret

    @validate_call
    def _parse_book_row(self, row: Any) -> Dict[str, str]:
        ret = {}
        col_displayname = self._find_element("book table row displayname column", "td.col-displayname", parent=row)
        ret["bookname"] = col_displayname.text
        col_contacts = self._find_element("book table row contacts column", "td.col-contacts", parent=row)
        ret["contacts"] = int(col_contacts.text)
        col_description = self._find_element("book table row description column", "td.col-description", parent=row)
        ret["description"] = col_description.text
        data = self._parse_row_info("addressbooks", row)
        ret.update(data)
        ret["token"] = ret["uri"].split("/")[-2]
        return ret

    @validate_call
    def _parse_row_info(self, name: str, row: Any) -> Dict[str, str]:
        actions = self._find_element(f"{name} table row actions column", "td.col-actions", parent=row)
        popover = self._find_element(f"{name} table row actions popover data", "span.btn.popover-hover", parent=actions)
        data_content = popover.get_attribute("data-content")
        soup = BeautifulSoup(data_content, "html.parser")
        ret = {}
        last_line = None
        for line in soup.strings:
            if last_line == "URI":
                ret["uri"] = line
            elif last_line == "User name":
                ret["username"] = line
            last_line = line
        if "uri" not in ret:
            raise BrowserInterfaceFailure(f"{name} table row info parse failed")
        return ret

    @validate_call
    def _row_action_buttons(self, name: str, row: Any) -> Dict[str, Any]:
        actions = self._find_element(f"{name} table row actions column", "td.col-actions", parent=row)
        action_buttons = self._find_elements(f"{name} table row actions buttons", "a.btn", parent=actions)
        buttons = {e.text: e for e in action_buttons if e.text}
        return buttons

    @validate_call
    def users(self, admin: Account) -> List[User]:
        self.logger.debug("request: users")
        self.login(admin)
        self._click_navbar_link("users", "Users and resources")
        rows = self._table_rows("users")
        user_list = [User(**self._parse_user_row(row)) for row in rows]
        self.logger.debug(f"users: returning {len(user_list)}")
        return user_list

    @validate_call
    def add_user(self, admin: Account, request: AddUserRequest) -> User:
        self.logger.debug(f"request: add_user {request.username} {request.displayname} ************")
        user = User(**request.model_dump())
        Accounts().set(user.username, request.password)
        self.login(admin)
        self._click_navbar_link("add_user", "Users and resources")
        self._click_button("add user button", "body .btn", with_text="+ Add user")
        self._set_text("add user username field", 'body form input[name="data[username]"]', user.username)
        self._set_text("add user displayname field", 'body form input[name="data[displayname]"]', user.displayname)
        self._set_text("add user email field", 'body form input[name="data[email]"]', user.username)
        self._set_text("add user password field", 'body form input[name="data[password]"]', request.password)
        self._set_text(
            "add user password confirmation field",
            'body form input[name="data[passwordconfirm]"]',
            request.password,
        )
        self._click_button(
            "add user save changes button",
            "body form .btn",
            with_text="Save changes",
        )
        self._check_add_popups("user", f"User {user.username} has been created.")
        _, parsed = self._find_user_row(user.username, allow_none=False)
        added = User(**parsed)
        if added.username == request.username and added.displayname == request.displayname:
            self.logger.debug("add_user: added")
            return added
        raise AddFailed(
            f"added user mismatches request: added={repr(added.model_dump())} request={repr(request.model_dump())}"
        )

    @validate_call
    def _check_add_popups(self, name: str, expected: str):
        popups = self._check_popups()
        self._click_button(f"add {name} close button ", "body form .btn", with_text="Close")
        if expected in popups:
            return
        elif popups:
            message = ": ".join(popups).replace("\n", ": ")
        else:
            message = "missing add response"
        self.logger.error(message)
        raise AddFailed(message)

    @validate_call
    def delete_user(self, admin: Account, request: DeleteUserRequest) -> Dict[str, str]:
        username = request.username
        self.logger.debug(f"request: delete_user {username}")
        self.login(admin)
        actions = self._find_user_actions(username)
        if not actions:
            raise DeleteFailed(f"user not found: {username=}")
        button = actions.get("Delete", None)
        if not button:
            raise BrowserInterfaceFailure("failed to locate Delete button")
        button.click()
        self._find_elements(
            "user delete confirmation button", "div.alert .btn-danger", with_text="Delete " + username, click=True
        )
        self._await_navbar_clickable()
        self.logger.debug("delete_user: deleted")
        Accounts.delete(username)
        return dict(message=f"deleted: {username}")

    @validate_call
    def _await_navbar_clickable(self):
        # wait for the navbar to become clickable - avoids breakage when deleting multple items
        wait = WebDriverWait(self.driver, timeout=POST_DELETE_TIMEOUT)
        wait.until(expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, 'body .navbar li a[href*="users"]')))

    @validate_call
    def _find_user_row(self, username: str, allow_none: bool | None = True) -> Tuple[Any | None, Any | None]:
        self._click_navbar_link("find_user_row", "Users and resources")
        rows = self._table_rows("users", allow_none=allow_none)
        for row in rows:
            user = self._parse_user_row(row)
            if user["username"] == username:
                return row, user
        self.logger.warning(f"user {username} not found")
        if allow_none:
            return None, None
        raise BrowserInterfaceFailure(f"failed to locate user row: {username=}")

    @validate_call
    def _find_user_actions(self, username: str, allow_none: bool | None = True) -> Dict[str, Any]:
        row, _ = self._find_user_row(username, allow_none=allow_none)
        if row:
            return self._row_action_buttons("user", row)
        return {}

    @validate_call
    def _select_user_address_books(self, username: str, allow_none: bool | None = True):
        buttons = self._find_user_actions(username, allow_none=allow_none)
        if buttons:
            buttons["Address Books"].click()
            return True
        return None

    @validate_call
    def _find_book_row(
        self, username: str, token: str, allow_none: bool | None = True
    ) -> Tuple[Any | None, Dict[str, Any] | None]:
        if not self._select_user_address_books(username, allow_none=allow_none):
            return None, None
        rows = self._table_rows("addressbooks")
        for row in rows:
            parsed = self._parse_book_row(row)
            if parsed["token"] == token:
                return row, parsed
        return None, None

    @validate_call
    def books(self, admin: Account, username: str) -> List[Book]:
        self.logger.debug(f"request: books {username}")
        self.login(admin)
        if not self._select_user_address_books(username):
            self.logger.debug("books: returning 0")
            return []
        rows = self._table_rows("addressbooks")
        ret = [Book(**self._parse_book_row(row)) for row in rows]
        self.logger.debug(f"books: returning {len(ret)}")
        return ret

    @validate_call
    def add_book(self, admin: Account, request: AddBookRequest) -> Book:
        self.logger.debug(f"request: add_book {request.username} {request.bookname} {request.description}")
        self.login(admin)
        user_row, _ = self._find_user_row(request.username)
        if user_row is None:
            raise AddFailed(f"user not found: username={request.username}")
        token = request.username + "-" + request.bookname
        token = "".join([c if c in VALID_TOKEN_CHARS else "-" for c in token])
        book = Book(token=token, **request.model_dump())

        row, _ = self._find_book_row(book.username, book.token)
        if row is not None:
            raise AddFailed(f"address book exists: username={book.username} token={book.token}")

        self._select_user_address_books(book.username)
        self._click_button("add address book button", "body .btn", with_text="+ Add address book")
        self._set_text("add book token field", 'body form input[name="data[uri]"]', book.token)
        self._set_text("add book name field", 'body form input[name="data[displayname]"]', book.bookname)
        self._set_text("add book description field", 'body form input[name="data[description]"]', book.description)
        self._click_button("add book save changes button", "body form .btn", with_text="Save changes")
        self._check_add_popups("addressbook", f"Address Book {book.bookname} has been created.")
        _, parsed = self._find_book_row(request.username, token, allow_none=False)
        added = Book(**parsed)
        if (
            added.username == request.username
            and added.bookname == request.bookname
            and added.description == request.description
            and added.token == token
        ):
            self.logger.debug("add_book: added")
            return added
        raise AddFailed(
            f"added book mismatches request: added={repr(added.model_dump())} request={repr(request.model_dump())}"
        )

    @validate_call
    def delete_book(self, admin: Account, request: DeleteBookRequest) -> Dict[str, str]:
        self.logger.debug(f"request: delete_book {request.username} {request.token}")
        self.login(admin)
        user_row, _ = self._find_user_row(request.username)
        if user_row is None:
            raise DeleteFailed(f"user not found: username={request.username}")
        row, book = self._find_book_row(request.username, request.token)
        if not row:
            raise DeleteFailed(f"book not found: username={request.username} token={request.token}")
        actions = self._row_action_buttons("addressbook", row)
        button = actions.get("Delete", None)
        if not button:
            raise BrowserInterfaceFailure("failed to locate address book Delete button")
        button.click()
        self._find_elements(
            "book delete confirmation button",
            "div.alert .btn-danger",
            with_text="Delete " + book["bookname"],
            click=True,
        )
        self._await_navbar_clickable()
        self.logger.debug("delete_book: deleted")
        return dict(message=f"deleted: {request.token}")

    @validate_call
    def reset(self, admin: Account) -> Dict[str, str]:
        self.logger.debug("request: reset")
        self.shutdown()
        self.login(admin)
        self.reset_time = arrow.now()
        self.logger.debug("request: reset complete")
        return dict(message="session reset")

    @validate_call
    def status(self, admin: Account) -> Dict[str, str]:
        self.logger.debug("request: status")

        try:
            self.login(admin)
            login = "success"
        except Exception as e:
            login = f"failed: {repr(e)}"

        state = dict(
            name="bcc",
            version=__version__,
            driver=repr(self.driver),
            url=settings.CALDAV_URL,
            uptime=self.startup_time.humanize(),
            reset=self.reset_time.humanize() if self.reset_time else "never",
            profile_dir=settings.PROFILE_NAME if self.profile else None,
            certificates=repr(list(self.profile.ListCerts().keys()) if self.profile else None),
            certificate_loaded=settings.CLIENT_CERT,
            login=login,
        )
        self.logger.debug("status: returning state")
        return state
