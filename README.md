# Waymap - Web Vulnerability Scanner (v2 - Yash Kulkarni)  

**Current Version**: 6.1.8  
**Original Author**: Trix Cyrus  
**Original Maintainers**: Yash Kulkarni & Jenin Sutradhar  
**Fork Maintainer**: Yash Kulkarni  
**Copyright**: © 2024 TrixSec Org  
**Maintained**: Yes  

![Waymap Logo](https://waymapscanner.github.io/images/waymap.jpg)  

## What is Waymap?  
Waymap is a high-speed web vulnerability scanner optimized for ethical hackers and penetration testers. It supports multiple scan types, customizable configurations, and can detect **75+ web vulnerabilities**. This fork builds upon the original project with ongoing improvements, optimizations, and additional testing.  

## 🚀 **Features and Enhancements in This Fork**  

### 🔹 **Custom Improvements**  
- Continued maintenance and updates.  
- Performance optimizations and bug fixes.  
- Additional security testing for better results.  

### 🔹 **Flexible Scanning Options**  
- **Target-based scanning:** Scan single or multiple targets (`--target`, `--multi-target`).  
- **Profile-based scanning:** Includes **high-risk, critical-risk, and deepscan** profiles for targeted assessments.  

### 🔹 **Enhanced Scan Types**  
- **SQL Injection (SQLi), Command Injection (CMDi), SSTI, XSS, LFI, Open Redirect, CRLF, CORS misconfigurations, and more.**  
- **WAF/IPS Detection** (160+ WAF types) with `--check-waf`.  

### 🔹 **Performance Boosting**  
- Multi-threading support for faster scans (`--threads`).  
- Improved crawling efficiency (`--crawl`).  

### 🔹 **Update & Maintenance**  
- Regular updates to ensure accuracy and security.  
- Easy version check with `--check-updates`.  

## 🛠️ **How to Use**  

### Basic Scanning  
```bash
python waymap.py --target https://example.com --scan {scan_type}
```  
```bash
python waymap.py --multi-target targets.txt --scan {scan_type}
```  
```bash
python waymap.py --target https://example.com --profile high-risk
```  

### Faster Scanning with Threads  
```bash
python waymap.py --crawl 3 --target https://example.com --scan xss --threads 10
```  

### Update Waymap  
```bash
python waymap.py --check-updates
```  

## 🌟 **Contribute & Connect**  
This fork is open for contributions and improvements. If you find any issues, report them here: [GitHub Issues](https://github.com/issues)  

🔹 **Fork, Star & Follow for Updates!**  
**Happy Hacking!** 🛡️🔥  
