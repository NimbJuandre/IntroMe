# IntroMe

Introduce yourself to the network by playing your favorite song on Spotify when you connect to the Wi-Fi.

## Getting Started

These instructions will help you set up and run the IntroMe project within a virtual environment. This ensures a clean and isolated environment for your project.

### Prerequisites

- [Python](https://www.python.org/downloads/) installed on your computer.

### Create a Virtual Environment

First, create a virtual environment for IntroMe:

```bash
python -m venv myenv
```

### Install Project Dependencies

With the virtual environment active, install the project dependencies from the requirements.txt file:
```bash
pip install -r requirements.txt
```

# Configuring IntroMe

Follow these steps to configure the "IntroMe" project, including creating a Spotify Developer App and adding your user devices and Spotify song URIs.

## 1. Create a Spotify Developer App

To enable Spotify integration in "IntroMe," you need to create a Spotify Developer App on the Spotify Developer Dashboard. Here's how to do it:

- Visit the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) in your web browser.

- Log in with your Spotify account or create one if you don't have an account.

- Click on the "Dashboard" link at the top of the page to access your developer dashboard.

- Click on the "Create an App" button.

- Enter the following details:
  - **App Name:** Enter a name for your app.
  - **App Description:** Provide a short description for your app.
  - **Website:** Leave this field empty.
  - **Redirect URI:** Enter `http://localhost/`.
  - Leave the "Bundle IDs" and "Android Packages" fields empty.

- Read and accept the Spotify Developer Terms of Service.

- Click the "Create" button to create your app.

You will be taken to your app's dashboard, where you can access your Client ID, Client Secret, and other app-related information.

## 2. Copy Configuration Details to `config.json`

- In your "IntroMe" project directory, locate the `config.json` file.

- Open the `config.json` file and add the following information:
  ```json
  {
      "spotify_client_id": "your_client_id",
      "spotify_client_secret": "your_client_secret",
      "spotify_redirect_uri": "http://localhost/"
  }
