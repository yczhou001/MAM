<p align="center">
    <a href="https://python.org" title="Go to Python homepage"><img src="https://img.shields.io/badge/Python-&gt;=3.x-blue?logo=python&amp;logoColor=white" alt="Made with Python"></a>
</p>

<p align="center">
    <img src="https://img.shields.io/badge/maintained-yes-2ea44f" alt="maintained - yes">
    <a href="/CONTRIBUTING.md" title="Go to contributions doc"><img src="https://img.shields.io/badge/contributions-welcome-2ea44f" alt="contributions - welcome"></a>
</p>

<p align="center">
    <a href="https://pypi.org/project/requests"><img src="https://img.shields.io/badge/dependency-requests-critical" alt="dependency - requests"></a>
    <a href="https://pypi.org/project/python-dotenv"><img src="https://img.shields.io/badge/dependency-python--dotenv-critical" alt="dependency - python-dotenv"></a>
</p>

<p align="center">
    <img width="700" src="https://raw.githubusercontent.com/RMNCLDYO/Google-Search-API-Wrapper/main/.github/logo.png">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/dynamic/json?label=Google+Search+API+Wrapper&query=version&url=https%3A%2F%2Fraw.githubusercontent.com%2FRMNCLDYO%2FGoogle-Search-API-Wrapper%2Fmain%2F.github%2Fversion.json" alt="Version">
</p>

## Overview
A simple python wrapper for Google's Search API, enabling programatic web and image searches.

## Key Features
- Web and image search functionality using Google Custom Search JSON API.
- Customizable search queries and result limits.
- Formatted search results including titles, links, snippets, and images.
- Error handling for missing credentials or invalid queries.

## Prerequisites
- `Python 3.x`

## Dependencies
The following Python packages are required:
- `requests`: For making HTTP requests to the Google API.
- `python-dotenv`: For loading environment variables from an `.env` file.

## Installation
To use this wrapper, clone the repository and install dependencies:
```bash
git clone https://github.com/RMNCLDYO/Google-Search-API-Wrapper.git
cd Google-Search-API-Wrapper
pip install -r requirements.txt
```

### Obtaining Google Custom Search API Credentials

#### Obtaining an API Key
1. Visit the [Programmable Search Engine](https://developers.google.com/custom-search/v1/introduction) introduction page.
2. Scroll down to the middle of the page and click on 'Get a Key' to generate your API key.

#### What is a Programmable Search Engine?
A Programmable Search Engine allows you to search google via the API, using Google's core search technology. You can customize it extensively, including the look and feel, search features, and even link it with Google Analytics for user behavior insights.

#### Creating a Programmable Search Engine
Before using the Google Custom Search API, you need to create a Programmable Search Engine. Follow these steps:

1. Visit the Programmable Search Engine [Control Panel](https://programmablesearchengine.google.com/controlpanel/all).
2. Name your search engine and specify what to search:
   - Choose specific sites or the entire web.
3. Set your search settings, such as enabling image search and/or SafeSearch.
4. Complete the reCAPTCHA verification and create your search engine.
5. Once created, find your Search Engine ID (cx parameter) in the Overview page's Basic section.

## Configuration
1. Once you've obtained your API key and CX id, add them to your `.env` file.
2. Create a new file named `.env` in the root directory, or rename the `example.env` file in the root directory of the project to `.env`.
3. Add your API key and CX id to the `.env` file as follows:
   ```
   api_key=your_api_key_here
   cx=your_cx_id_here
   ```
4. The application will automatically load and use the API key and CX id when making API requests.

## Usage

#### Text Search Example

```python
from google_search_api import GoogleSearchAPI

print(GoogleSearchAPI().response(method='text', max_results=5, query='Your text prompt'))
```

#### Image Search Example

```python
from google_search_api import GoogleSearchAPI

print(GoogleSearchAPI().response(method='image', max_results=5, query='Your image prompt'))
```

## Contributing
Contributions are welcome!

Please refer to [CONTRIBUTING.md](.github/CONTRIBUTING.md) for detailed guidelines on how to contribute to this project.

## Reporting Issues
Encountered a bug? We'd love to hear about it. Please follow these steps to report any issues:

1. Check if the issue has already been reported.
2. Use the [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md) template to create a detailed report.
3. Submit the report [here](https://github.com/RMNCLDYO/Google-Search-API-Wrapper/issues).

Your report will help us make the project better for everyone.

## Feature Requests
Got an idea for a new feature? Feel free to suggest it. Here's how:

1. Check if the feature has already been suggested or implemented.
2. Use the [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md) template to create a detailed request.
3. Submit the request [here](https://github.com/RMNCLDYO/Google-Search-API-Wrapper/issues).

Your suggestions for improvements are always welcome.

## Versioning and Changelog
Stay up-to-date with the latest changes and improvements in each version:

- [CHANGELOG.md](.github/CHANGELOG.md) provides detailed descriptions of each release.

## Security
Your security is important to us. If you discover a security vulnerability, please follow our responsible disclosure guidelines found in [SECURITY.md](.github/SECURITY.md). Please refrain from disclosing any vulnerabilities publicly until said vulnerability has been reported and addressed.

## License
Licensed under the MIT License. See [LICENSE](LICENSE) for details.
