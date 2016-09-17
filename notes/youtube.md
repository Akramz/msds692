# YouTube

YouTube, like Zillow, will allow us to use its data spigot without authentication, but we must create a secret ID or key as we did before:

> If your client application does not use OAuth 2.0, then it must include an API key when it calls an API that's enabled within a Google Cloud Platform project. The application passes this key into all API requests as a key=API_key parameter. API keys do not grant access to any account information, and are not used for authorization.

Follow these steps to get set up:
 
1. [Get a google account](https://www.google.com/accounts) if you don't already have one.
2. Go to the [Google API Console](https://console.developers.google.com/) and create a project. I call mine msan692-test or something like that.
3. Enable the "YouTube Data API v3" API from your console.

Familiarize yourself with the [API documentation](https://developers.google.com/youtube/v3/) and install some Python code that will make our lives easier:

```bash
$ pip install --upgrade google-api-python-client
```

## First contact


