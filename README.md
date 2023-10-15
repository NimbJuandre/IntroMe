# IntroMe

Introduce yourself to the network by playing your favorite song on Spotify when you connect to the Wi-Fi.
You can choose to play your song on available devices in your network (Spotify does not show all devices, e.g., 3rd party speakers.)

## Getting Started

These instructions will help you set up and run the IntroMe project within a virtual environment. This ensures a clean and isolated environment for your project.

### Prerequisites

- [Python](https://www.python.org/downloads/) installed on your computer.

### Create a Virtual Environment

First, create a virtual environment for IntroMe:

```bash
python -m venv myenv
```
Then activate the virtual environment

```bash
myenv\Scripts\activate
```
### Install Project Dependencies

With the virtual environment active, install the project dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

# Configuring IntroMe

Follow these steps to configure the "IntroMe" project, including creating a Spotify Developer App and adding your user devices and Spotify song URIs to the config.

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
  - **Bundle IDs:** Leave this field empty.
  - **Android Packages:** Leave this field empty.

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

## 3. Add User Devices and Spotify Song URIs
To make "IntroMe" play your favorite song when you connect to Wi-Fi, you need to provide details about your user devices and Spotify song URIs. Follow these steps:

Get Your Device Wi-Fi MAC Address:

Determine the MAC address of the Wi-Fi device (ex. phone) you want to use as the trigger for playing music with "IntroMe."

Get a Spotify Song URI:

Find the Spotify song you want to play and copy its Spotify URI. You can do this on Windows by:

Holding down Ctrl + Alt and right-clicking on the song.
Select "Share" and then choose "Copy Spotify URI."
In your config.json file, add the following details:

```json
{
    "spotify_client_id": "your_client_id",
    "spotify_client_secret": "your_client_secret",
    "spotify_redirect_uri": "http://localhost/",
    "user_devices": [
        {
            "wifi_mac_address": "device wifi_mac_address",
            "spotify_song_uri": "spotify_song_uri"
        },
         {
            "wifi_mac_address": "device wifi_mac_address",
            "spotify_song_uri": "spotify_song_uri"
        },
         {
            "wifi_mac_address": "device wifi_mac_address",
            "spotify_song_uri": "spotify_song_uri"
        },
    ]
}
```
Replace "your_wifi_mac_address" and "your_spotify_song_uri" with the actual MAC address of your Wi-Fi device and the Spotify URI of your chosen song. There can be multiple user devices setup.

## Running the wifi listener script
```bash
python .\wifi_listener.py
```

That's it! You've successfully configured "IntroMe" with your Spotify Developer App, user devices, and Spotify song URIs. Enjoy introducing yourself to the network with your favorite tunes!
