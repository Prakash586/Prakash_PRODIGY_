<h1 align="center">🔐 PRODIGY Internship — Security Projects</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Internship-PRODIGY%20InfoTech-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Domain-Cybersecurity-red?style=for-the-badge&logo=hackthebox&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge"/>
</p>

---

## 📌 About This Repository

This repository contains all security-focused projects completed during my **PRODIGY InfoTech Cybersecurity Internship**.
Each project was built to develop hands-on offensive security and Python programming skills — covering cryptography, network analysis, system monitoring, and steganography.

---

## 🗂️ Projects Overview

| # | Project | Description | Key Concepts |
|---|---|---|---|
| 01 | 🔡 [Caesar Cipher](#-01---caesar-cipher) | Encrypt & decrypt text using the Caesar substitution cipher | Cryptography, Python |
| 02 | 🖼️ [Pixel Manipulation](#-02---pixel-manipulation--image-encryption) | Image encryption via pixel-level manipulation | Steganography, PIL |
| 03 | 🔑 [Password Strength Analyzer](#-03---password-strength-analyzer) | Evaluate password entropy, complexity & policy compliance | Security tooling, Python |
| 04 | 🎹 [Keylogger](#-04---keylogger) | Capture & log keystrokes for security research purposes | System monitoring, pynput |
| 05 | 📡 [Packet Sniffer](#-05---network-packet-sniffer) | Real-time packet capture with protocol inspection | Network security, Scapy |

---

## 🔡 01 - Caesar Cipher

**File:** `Caesar_Cipher.py`

A Python implementation of the classic Caesar cipher — encrypts and decrypts messages by shifting characters a configurable number of positions in the alphabet.

**What it does:**
- Accepts plaintext input and a shift key
- Encrypts text using character rotation
- Decrypts ciphertext back to plaintext
- Handles both uppercase and lowercase letters

**Concepts covered:** Substitution cryptography, modular arithmetic, Python string manipulation

---

## 🖼️ 02 - Pixel Manipulation / Image Encryption

**File:** `pixel_manipulation.py`

An image encryption tool that manipulates pixel RGB values to visually scramble an image — demonstrating how steganography and visual data obfuscation work.

**What it does:**
- Reads image pixel data
- Applies transformation logic to encrypt/hide visual content
- Reverses transformation to decrypt/restore the image

**Concepts covered:** Steganography, PIL/Pillow, pixel-level data manipulation

---

## 🔑 03 - Password Strength Analyzer

**File:** `Password_Strength.py`

A policy-driven password analysis tool that evaluates passwords against configurable security rules — useful for developer security tooling and security awareness.

**What it does:**
- Checks length, character classes, entropy
- Flags weak patterns (dictionary words, sequences)
- Returns a strength score with improvement suggestions

**Concepts covered:** Entropy analysis, regex, security policy enforcement

---

## 🎹 04 - Keylogger

**File:** `Keylogger.py`

> ⚠️ **For educational and authorized security research use only.**

A Python-based keylogger that captures and logs keystrokes — built to understand how malware monitors user input and how defenders can detect such activity.

**What it does:**
- Captures real-time keystrokes using `pynput`
- Logs input to a file for analysis
- Demonstrates attacker techniques for security awareness

**Concepts covered:** System monitoring, pynput, ethical offensive research

---

## 📡 05 - Network Packet Sniffer

**File:** `Packet_sniffer.py`

A real-time network packet capture and inspection tool built with Python and Scapy — designed as a preparation and learning tool for network security assessments.

**What it does:**
- Captures live network packets
- Filters by protocol (TCP, UDP, ICMP)
- Extracts and displays headers and payloads
- Flags anomalous or suspicious traffic patterns

**Concepts covered:** Network security, Scapy, protocol analysis, traffic inspection

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Scapy](https://img.shields.io/badge/Scapy-Network%20Analysis-004170?style=for-the-badge)
![Pillow](https://img.shields.io/badge/Pillow-Image%20Processing-yellow?style=for-the-badge)
![pynput](https://img.shields.io/badge/pynput-Input%20Monitoring-red?style=for-the-badge)

---

## ⚠️ Disclaimer

> All tools in this repository were built strictly for **educational purposes** as part of an authorized internship program.
> They are intended to demonstrate security concepts and support ethical research only.
> **Do not use these tools on systems or networks without explicit written authorization.**

---

## 👤 Author

**Prakash Chauhan** — Offensive Security Analyst
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/prakash-chauhan-1b50a822b)
[![GitHub](https://img.shields.io/badge/GitHub-Prakash586-181717?style=for-the-badge&logo=github)](https://github.com/Prakash586)
