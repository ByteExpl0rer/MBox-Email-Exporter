# MBox Email Exporter

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)

MBox Email Exporter is a Python script to analyze **mbox** email archives and generate a summary of emails per sender. Each CSV export is automatically placed in a **dated subfolder** for better organization.

---

## Features

- Count the number of emails sent by each sender.
- Compact terminal summary of senders.
- Automatic CSV export.
- Each export is placed in a **dated subfolder** to avoid overwriting previous exports.
- Handles email encodings robustly (UTF-8, MIME, etc.).
- Flexible: specify export folder and/or CSV filename.

---

## Requirements

- Python 3.x
- Standard Python libraries (no extra installation required)

---

## Installation

1. Clone the repository:  

```bash
git clone https://github.com/ByteExpl0rer/MBox-Email-Exporter.git
