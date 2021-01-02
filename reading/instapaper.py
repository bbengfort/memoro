# reading.instapaper
# Client for the Instapaper API
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 01 09:05:38 2021 -0500
#
# Copyright (C) 2020 Bengfort.com
# For license information, see LICENSE
#
# ID: instapaper.py [] benjamin@bengfort.com $

"""
Client for the Instapaper API (https://www.instapaper.com/api/full)
"""

##########################################################################
## Imports
##########################################################################

import os
import json
import oauth2 as oauth

from datetime import datetime, timezone
from urllib.parse import urljoin, urlencode, parse_qsl

try:
    from django.conf import settings
except ImportError:
    settings = None


ENDPOINT = "https://www.instapaper.com/api/1/"
CONSUMER_ID_ENVVAR="INSTAPAPER_CONSUMER_ID"
CONSUMER_SECRET_ENVVAR = "INSTAPAPER_CONSUMER_SECRET"


##########################################################################
## Instapaper Client
##########################################################################

class Instapaper(object):
    """
    Initialize the Instapaper API client with an Oauth1 consumer id and seceret. If not
    supplied, the object looks in the django settings and then in the environment for
    the keys, otherwise raises an improperly configured exception.
    """

    @classmethod
    def cached_access_token(
        cls, oauth_token, oauth_token_secret, client_key=None, client_secret=None
    ):
        """
        Initialize API client with cached access token to prevent reauthentication.
        """
        client = cls(client_key=client_key, client_secret=client_secret)
        consumer = oauth.Consumer(client.client_key, client.client_secret)
        access_token = oauth.Token(oauth_token, oauth_token_secret)
        client.session = oauth.Client(consumer, access_token)
        client.session.set_signature_method = oauth.SignatureMethod_HMAC_SHA1()
        return client

    def __init__(self, client_key=None, client_secret=None):
        if client_key is None:
            if settings and settings.INSTAPAPER_CONSUMER_ID:
                client_key = settings.INSTAPAPER_CONSUMER_ID
            else:
                client_key = os.getenv(CONSUMER_ID_ENVVAR)

        if client_secret is None:
            if settings and settings.INSTAPAPER_CONSUMER_SECRET:
                client_secret = settings.INSTAPAPER_CONSUMER_SECRET
            else:
                client_secret = os.getenv(CONSUMER_SECRET_ENVVAR)

        if not client_key or not client_secret:
            raise InstapaperException(
                1038, "client oauth consumer id and secret required"
            )

        self.client_key = client_key
        self.client_secret = client_secret
        self.session = None

    def authenticate(self, username, password):
        """
        All API interactions must happen through authenticated sessions that are
        constructed using an xAuth workflow. This endpoint authenticates the a user with
        their username and password and creates the session for other requests.
        """
        consumer = oauth.Consumer(self.client_key, self.client_secret)
        client = oauth.Client(consumer)
        client.add_credentials("username", "password")
        client.authorizations

        creds = {
            "x_auth_username": username,
            "x_auth_password": password,
            "x_auth_mode": "client_auth"
        }

        token_url = self._endpoint("oauth/access_token")
        client.set_signature_method = oauth.SignatureMethod_HMAC_SHA1()
        rep, content = client.request(token_url, method="POST", body=urlencode(creds))

        if rep.status < 200 or rep.status >= 300:
            raise HTTPException(rep, content)

        try:
            token = dict(parse_qsl(content.decode('UTF-8')))
            for field in ("oauth_token", "oauth_token_secret"):
                if field not in token:
                    raise KeyError(f"missing required key {field}")
        except Exception as e:
            raise HTTPException(rep, content) from e

        access_token = oauth.Token(token["oauth_token"], token["oauth_token_secret"])
        self.session = oauth.Client(consumer, access_token)
        self.session.set_signature_method = oauth.SignatureMethod_HMAC_SHA1()
        return token

    def verify_credentials(self):
        """
        Returns the currently logged in user.
        """
        return self._post("account/verify_credentials")

    def bookmarks(self, limit=25, folder_id="unread", have="", highlights=""):
        """
        Lists the user's unread bookmarks, and can also synchronize reading positions.

        Parameters
        ----------
        limit : int (default=25, optional)
            A number between 1 and 500, default 25.

        folder_id : str (default=unread, optional)
            Possible values are unread (default), starred, archive, or a folder_id value
            from /api/1.1/folders/list.

        have : str (optional)
            A concatenation of bookmark_id values that the client already has from the
            specified folder. This is a comma-separated list of bookmark_id values that
            the client already has in its local bookmark data, and shouldn't be re-sent.
            Any IDs sent in the have parameter that would not have appeared in the list
            within the given limit are returned in a delete_ids parameter on the meta
            object. See the documentation for more details.

        highlights : str (optional)
            A '-' delimited list of highlight IDs that the client already has from
            the specified bookmarks.
        """
        params = {
            "limit": limit,
            "folder_id": folder_id,
            "have": have,
            "highlights": highlights
        }
        return self._post("bookmarks/list", params)

    def update_read_progress(self, bookmark_id, progress, timestamp=None):
        """
        Updates the user's reading progress on a single article. This functionality is
        included in the have parameter of the /api/1.1/bookmarks/list operation above,
        but this method exists in case you want to call it separately.

        Parameters
        ----------
        bookmark_id : int
            The bookmark to update.

        progress : float
            The user's progress, as a floating-point number between 0.0 and 1.0, defined
            as the top edge of the user's current viewport, expressed as a percentage of
            the article's total length.

        timestamp: datetime, optional
            The  value of the time that the progress was recorded.
        """
        if timestamp is None:
            timestamp = datetime.now(tz=timezone.utc)
        timestamp = timestamp.timestamp()

        params = {
            "bookmark_id": bookmark_id,
            "progress": progress,
            "progress_timestamp": timestamp,
        }

        return self._post("bookmarks/update_read_progress", params)

    def add_bookmark(
        self,
        url,
        title=None,
        description=None,
        folder_id=None,
        resolve_final_url=1,
        content=None,
        is_private_from_source=None,
    ):
        """
        Adds a new unread bookmark to the user's account.

        Parameters
        ----------
        url : str
            Required, except when using private sources (see documentation).

        title : str (optional)
            If omitted or empty, the title will be looked up by Instapaper
            synchronously. This will delay the action, so please specify the title if
            you have it.

        description : str (optional)
            A brief, plaintext description or summary of the article. Twitter clients
            often put the source tweet's text here, and Instapaper's bookmarklet puts
            the selected text here if the user has selected any.

        folder_id : int (optional)
            The integer folder ID as returned by the folders/list method.

        resolve_final_url : int (default=1)
            Specify 1 if the url might not be the final URL that a browser would resolve
            when fetching it, such as if it's a shortened URL, it's a URL from an RSS
            feed that might be proxied, or it's likely to go through any other
            redirection when viewed in a browser. This will cause Instapaper to attempt
            to resolve all redirects itself, synchronously. This will delay the action,
            so please specify 0 for this parameter if you're reasonably confident that
            this URL won't be redirected, such as if it's already being viewed in a
            web browser.

        content :  str (optional)
            You can optionally supply the full HTML content of pages that Instapaper
            wouldn't otherwise be able to crawl from its servers, such as pages that
            require logins or Instapaper Premium. The full HTML content of the page, or
            just the <body> node's content if possible, such as the value of
            document.body.innerHTML in Javascript. Must be UTF-8.

        is_private_from_source : str (optional)
            Bookmarks can be private, such as the bookmarks that result from
            Instapaper's  feature. Private bookmarks are not shared to other users
            through any sharing functionality (such as Starred-folder subscriptions),
            and they do not have URLs. A short description label of the source of the
            private bookmark, such as "email" or "MyNotebook Pro". When using this,
            values passed to url will be ignored, and the content parameter is required.
        """
        params = {
            "url": url, "title": title, "description": description,
            "folder_id": folder_id, "resolve_final_url": resolve_final_url,
        }

        if content is not None:
            params["content"] = content

        if is_private_from_source is not None:
            content["is_private_from_source"] = is_private_from_source

        return self._post("bookmarks/add", params)

    def delete_bookmark(self, bookmark_id):
        """
        Permanently deletes the specified bookmark. This is NOT the same as Archive.
        Please be clear to users if you're going to do this.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post("bookmarks/delete", {"bookmark_id": bookmark_id})

    def star(self, bookmark_id):
        """
        Stars the specified bookmark.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post("bookmarks/star", {"bookmark_id": bookmark_id})

    def unstar(self, bookmark_id):
        """
        Un-stars the specified bookmark.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post("bookmarks/unstar", {"bookmark_id": bookmark_id})

    def archive(self, bookmark_id):
        """
        Moves the specified bookmark to the Archive.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post("bookmarks/archive", {"bookmark_id": bookmark_id})

    def unarchive(self, bookmark_id):
        """
        Moves the specified bookmark to the top of the Unread folder.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post("bookmarks/unarchive", {"bookmark_id": bookmark_id})

    def move(self, bookmark_id, folder_id):
        """
        Moves the specified bookmark to a user-created folder.

        Parameters
        ----------
        bookmark_id : int, required

        folder_id : int, required
        """
        params = {"bookmark_id": bookmark_id, "folder_id": folder_id}
        return self._post("bookmarks/move", params)

    def get_text(self, bookmark_id):
        """
        Returns the specified bookmark's processed text-view HTML, which is always
        text/html encoded as UTF-8.

        Parameters
        ----------
        bookmark_id : int, required

        Output: HTML with an HTTP 200 OK status, not the standard API output structures,
        or an HTTP 400 status code and a standard error structure if anything goes wrong.
        """
        if self.session is None:
            raise InstapaperException(1039, "client has not been authenticated")

        # NOTE: for signature to be correct, we cannot set a content-type here.
        headers = {
            "Accept": "text/html",
            "User-Agent": "Memoro Instapaper API Client (Python)",
        }

        data = {"bookmark_id": bookmark_id}
        body = json.dumps(data, ensure_ascii=False).encode('UTF-8') if data else b''
        rep, content = self.session.request(
            self._endpoint("bookmarks/get_text"),
            method="POST",
            body=body,
            headers=headers
        )

        if rep.status == 200:
            # We've got the text and it's good, so return it decoded
            return content.decode('UTF-8')

        # Otherwise this is an exception
        try:
            # If we cannot parse the json data, raise an HTTPException
            content = json.loads(content, encoding='UTF-8')
        except Exception as e:
            raise HTTPException(rep, content) from e

        # Attempt to raise InstapaperException, otherwise raise http exception
        self._handle_error(content)
        raise HTTPException(rep, content)

    def folders(self):
        """
        A list of the account's user-created folders. This only includes organizational
        folders and does not include RSS-feed folders or starred-subscription folders,
        as the implementation of those is changing in the near future.
        """
        return self._post("folders/list")

    def add_folder(self, title):
        """
        Creates an organizational folder.

        Parameters
        ----------
        title : str, required
        """
        return self._post("folders/add", {"title": title})

    def delete_folder(self, folder_id):
        """
        Deletes the folder and moves any articles in it to the Archive.

        Parameters
        ----------
        folder_id : int, required
        """
        return self._post("folders/delete", {"folder_id": folder_id})

    def set_folder_order(self, order):
        """
        Re-orders a user's folders.

        Parameters
        ----------
        order : str, required
            A set of folder_id:position pairs joined by commas, where the position is a
            positive integer 32 bits or less. Example input, given the folder_ids 100,
            200, and 300, wanting to order them in that order:

                100:1,200:2,300:3

            Or, to reverse their order:

                100:3,200:2,300:1

            The order of the pairs doesn't matter, only the position values do, so this
            is equivalent to the above value:

                300:1,100:3,200:2

            You must include all of the user's folders for consistent ordering. Invalid
            or missing folder IDs or positions will be ignored and will not return
            errors.
        """
        return self._post("folders/set_order", {"order": order})

    def highlights(self, bookmark_id):
        """
        List highlights for <bookmark-id>

        Warning: HTML in highlight text is returned unescaped through the API.

        Parameters
        ----------
        bookmark_id : int, required
        """
        return self._post(f"/api/1.1/bookmarks/{bookmark_id}/highlights")

    def add_highlight(self, bookmark_id, text, position=0):
        """
        Create a new highlight for <bookmark-id>

        HTML tags in text parameter should be unescaped.

        Note: Non-subscribers are limited to 5 highlights per month.

        Parameters
        ----------
        bookmark_id : int, required

        text : str, required
            The text for the highlight

        position : int (default=0, optional)
            The 0-indexed position of text in the content.
        """
        params = {"text": text, "position": position}
        return self._post(f"/api/1.1/bookmarks/{bookmark_id}/highlight", params)

    def delete_highlight(self, highlight_id):
        """
        Delete a highlight

        Parameters
        ----------
        highlight_id : int, required
        """
        return self._post(f"/api/1.1/highlights/{highlight_id}/delete")

    def _post(self, path, data=None):
        if self.session is None:
            raise InstapaperException(1039, "client has not been authenticated")

        # NOTE: for signature to be correct, we cannot set a content-type here.
        headers = {
            "Accept": "application/json",
            "User-Agent": "Memoro Instapaper API Client (Python)",
        }

        # body = json.dumps(data, ensure_ascii=False).encode('UTF-8') if data else b''
        from urllib.parse import urlencode
        body = urlencode({key: str(val) for key, val in data.items()}) if data else b''
        rep, content = self.session.request(
            self._endpoint(path), method="POST", body=body, headers=headers
        )

        # Received a non-200 response, raise an exception
        if rep.status < 200 or rep.status >= 300:
            raise HTTPException(rep, content)

        try:
            # If we cannot parse the json data, raise an HTTPException
            content = json.loads(content, encoding='UTF-8')
        except Exception as e:
            raise HTTPException(rep, content) from e

        self._handle_error(content)
        return content


    def _handle_error(self, content):
        if isinstance(content, list):
            # TODO: handle case where there is error and meta together
            if len(content) == 1 and content[0].get("type", None) == "error":
                raise InstapaperException(
                    content[0]["error_code"], content[0]["message"]
                )
        elif isinstance(content, dict):
            if content.get("type", None) == "error":
                raise InstapaperException(content["error_code"], content["message"])

    def _endpoint(self, path):
        """
        Returns an endpoint for the specified relative path.
        """
        return urljoin(ENDPOINT, path)


class InstapaperException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return f"{self.code}: {self.message}"


class HTTPException(InstapaperException):

    def __init__(self, response, body):
        self.response = response
        self.body = body

    def __str__(self):
        return f"{self.response.status} {self.response.reason}"
