<h1 align="left" style="margin-bottom: 20px; font-weight: 500; font-size: 50px; color: black;">
  FastAPI JWT Auth
</h1>

[![Tests](https://github.com/LibreNZ/libre-fastapi-jwt/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/LibreNZ/libre-fastapi-jwt/actions/workflows/tests.yml)
[![CodeQL](https://github.com/LibreNZ/libre-fastapi-jwt/actions/workflows/codeql.yml/badge.svg)](https://github.com/LibreNZ/libre-fastapi-jwt/actions/workflows/codeql.yml)
[![PyPI version](https://badge.fury.io/py/libre-fastapi-jwt.svg)](https://badge.fury.io/py/libre-fastapi-jwt)
[![Downloads](https://static.pepy.tech/personalized-badge/libre-fastapi-jwt?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/libre-fastapi-jwt)

---


**Documentation**: <a href="https://LibreNZ.github.io/libre-fastapi-jwt" target="_blank">https://LibreNZ.github.io/libre-fastapi-jwt</a>

**Source Code**: <a href="https://github.com/LibreNZ/libre-fastapi-jwt" target="_blank">https://github.com/LibreNZ/libre-fastapi-jwt</a>

---
>This project was originally based on <a href="https://github.com/IndominusByte/fastapi-jwt-auth" target="_blank">fastapi-jwt-auth</a> 
---

## Features
FastAPI extension that provides JWT Auth support (secure, easy to use and lightweight), if you were familiar with flask-jwt-extended this extension suitable for you, cause this extension inspired by flask-jwt-extended 😀

- Integrated with the <img src="docs/image.png" alt="drawing" width="100" style="align: center; margin: auto; "/> button
- Access tokens and refresh tokens
- Freshness Tokens
- Revoking Tokens
- Dual Tokens (cookie and headers)
- Support for WebSocket authorization
- Support for adding custom claims to JSON Web Tokens
- Storing tokens in cookies and CSRF protection

## Installation
The easiest way to start working with this extension with pip

```bash
pip install libre-fastapi-jwt
```

If you want to use asymmetric (public/private) key signing algorithms, include the <b>asymmetric</b> extra requirements.
```bash
pip install 'libre-fastapi-jwt[asymmetric]'
```

## License
This project is licensed under the terms of the MIT license.
