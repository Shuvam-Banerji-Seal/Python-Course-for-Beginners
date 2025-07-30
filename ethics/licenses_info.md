# Common Open-Source Licenses Cheat-Sheet

| License | Full Name | Latest Version | Type | Copyleft / Permissive | Patent Grant | Trademark Grant | State Changes | Liability & Warranty | Typical Use-Cases |
|---------|-----------|----------------|------|-----------------------|--------------|-----------------|---------------|----------------------|-------------------|
| **MIT** | MIT License | – | Permissive | Permissive | ❌ | ❌ | ❌ | ✔ (disclaimed) | Libraries, tools, almost everything |
| **GPL-2.0** | GNU General Public License v2 | 2.0 | Copyleft (Strong) | ✔ | ✔ | ❌ | ✔ | ✔ (disclaimed) | Linux kernel, older GNU projects |
| **GPL-3.0** | GNU General Public License v3 | 3.0 | Copyleft (Strong) | ✔ | ✔ | ❌ | ✔ | ✔ (disclaimed) | GNU software, GCC, many apps |
| **LGPL-2.1** | GNU Lesser General Public License v2.1 | 2.1 | Copyleft (Weak) | Partial | ✔ | ❌ | ✔ | ✔ (disclaimed) | Libraries that may be linked by proprietary code |
| **LGPL-3.0** | GNU Lesser General Public License v3 | 3.0 | Copyleft (Weak) | Partial | ✔ | ❌ | ✔ | ✔ (disclaimed) | Same as above, newer projects |
| **AGPL-3.0** | GNU Affero General Public License v3 | 3.0 | Copyleft (Network) | ✔ (network use triggers) | ✔ | ❌ | ✔ | ✔ (disclaimed) | SaaS/web applications |
| **Apache-2.0** | Apache License 2.0 | 2.0 | Permissive | Permissive | ✔ | ✔ | ✔ | ✔ (disclaimed) | Big-data, Android, corporate projects |
| **BSD-2-Clause** | 2-Clause BSD License | – | Permissive | Permissive | ❌ | ❌ | ❌ | ✔ (disclaimed) | Minimal, widely compatible |
| **BSD-3-Clause** | 3-Clause BSD License | – | Permissive | Permissive | ❌ | ✔ (no endorsement) | ❌ | ✔ (disclaimed) | Same as BSD-2, plus no-name clause |
| **ISC** | Internet Systems Consortium License | – | Permissive | Permissive | ❌ | ❌ | ❌ | ✔ (disclaimed) | Drop-in replacement for MIT/BSD |
| **CC0-1.0** | Creative Commons Zero v1.0 Universal | 1.0 | Public Domain Dedication | N/A | ❌ | ❌ | ❌ | ✔ (waived) | Data, documentation, artwork |
| **CC-BY-4.0** | Creative Commons Attribution 4.0 International | 4.0 | Permissive (Creative Commons) | Permissive | ❌ | ✔ (BY) | ✔ | ✔ (disclaimed) | Open-access papers, media |
| **CC-BY-SA-4.0** | Creative Commons Attribution-ShareAlike 4.0 | 4.0 | Copyleft (Creative Commons) | ✔ | ❌ | ✔ (BY-SA) | ✔ | ✔ (disclaimed) | Wikipedia, open educational content |
| **CC-BY-NC-4.0** | Creative Commons Attribution-NonCommercial 4.0 | 4.0 | Non-commercial | Restrictive | ❌ | ✔ (BY-NC) | ✔ | ✔ (disclaimed) | Non-commercial art, learning material |
| **CC-BY-ND-4.0** | Creative Commons Attribution-NoDerivatives 4.0 | 4.0 | Restrictive | Restrictive (no mods) | ❌ | ✔ (BY-ND) | ✔ | ✔ (disclaimed) | Press releases, official statements |
| **EPL-2.0** | Eclipse Public License 2.0 | 2.0 | Weak Copyleft | Partial | ✔ | ❌ | ✔ | ✔ (disclaimed) | Eclipse IDE, Java projects |
| **MPL-2.0** | Mozilla Public License 2.0 | 2.0 | Weak Copyleft | Partial | ✔ | ❌ | ✔ | ✔ (disclaimed) | Firefox, Thunderbird |
| **Unlicense** | The Unlicense | – | Public Domain Dedication | N/A | ❌ | ❌ | ❌ | ✔ (waived) | Tiny utilities, snippets |

### Quick Usage Tips
- **Permissive (MIT/BSD/Apache-2.0/ISC)**  
  – Easy to integrate in proprietary products.  
  – Only requirement: keep copyright notice & license text.

- **Copyleft (GPL-family/LGPL/MPL/EPL)**  
  – Derivative works must be released under the same or compatible license.  
  – LGPL/Weak Copyleft allows linking in proprietary apps.

- **Creative Commons (CC)**  
  – **Best for non-code assets** (docs, images).  
  – **Avoid** for software; use OSI-approved licenses instead.

- **Public Domain (CC0 / Unlicense)**  
  – No restrictions; worldwide public domain waiver.  
  – May still have patent issues; Apache-2.0 offers clearer patent grant.

> Always include the full license text (`LICENSE` or `COPYING`) in your repository root and add a SPDX identifier in each source file header:  
> `// SPDX-License-Identifier: MIT`
