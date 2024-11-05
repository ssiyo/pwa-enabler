# PWA Enabler Script

This Python script automates the process of converting a standard web project into a Progressive Web App (PWA).  It handles the creation and placement of necessary files like `app.webmanifest`, `register-sw.js`, and `sw.js`,  modifying existing HTML files, and generating a service worker configuration to enable offline capabilities.

## How it Works

The script takes the path to your web project directory as input. It then performs the following steps:

1. **Project Analysis:**  The script analyzes the project directory structure, identifying HTML files and other assets. It also gathers information such as the project name (derived from the directory name) and the current date for cache versioning.

2. **File Generation:**
    * **`app.webmanifest`:**  Creates a `app.webmanifest` file containing essential PWA metadata like the app name, icons, display mode, and background/theme colors.
    * **`register-sw.js`:** Generates a `register-sw.js` script to register the service worker in the browser.
    * **`sw.js`:**  Creates the `sw.js` service worker file, which includes logic for caching files and handling offline requests. This file includes a dynamically generated list of files to cache based on the project's contents.

3. **HTML Modification:**  The script injects the necessary `<link>` tag for the `app.webmanifest` into the `<head>` of all HTML files within the project. It also adds the `<script>` tag for the `register-sw.js` file to the `<head>` of the `index.html` file.

4. **Cache Configuration:** The `sw.js` file is configured to cache all essential project files, ensuring offline access. The script automatically generates the list of files to be cached based on the directory structure. The cache is versioned using the current date to facilitate updates.

## Usage

1. **Prerequisites:** Make sure you have Python installed.

2. **Installation:** Install the package locally to make the script callable anywhere (from any directory).

```bash
pip install dist/pwa_enabler-1.0.4-py3-none-any.whl
```

3. **Run the script:** Execute the script, providing the absolute or **relative** path to your web project directory as an argument:

```bash
pwa-enabler /path/to/your/web/project
```

4. **Verify the changes:** Check your project directory for the newly created files (`app.webmanifest`, `register-sw.js`, `sw.js`) and the modifications made to the HTML files.

## Example

```bash
pwa-enabler ./my-web-app
```

This command will process the `my-web-app` directory and convert it into a PWA.
