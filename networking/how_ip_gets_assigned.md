
flowchart TD
    A[User turns on WiFi device] --> B[Device sends DHCP Discover as broadcast]
    B --> C[Router receives discover and checks DHCP pool]
    C --> D[Router sends DHCP Offer with private IP like 192.168.1.10]
    D --> E[Device sends DHCP Request to confirm offer]
    E --> F[Router sends DHCP Ack and assigns private IP]

    F --> G[Router checks WAN connection]
    G --> H[Router sends DHCP Discover to ISP server]
    H --> I[ISP server replies with DHCP Offer with public IP]
    I --> J[Router sends DHCP Request for offered IP]
    J --> K[ISP sends DHCP Ack and assigns public IP like 103.12.44.6]

    K --> L[Router uses NAT to map device private IP to public IP]
    L --> M[Device accesses internet via NAT]

    subgraph Fallbacks
        N1[If no DHCP response from router]
        N2[Device assigns link-local IP like 169.254 dot x dot x]
        N3[Limited local network access only]

        N4[If no IP from ISP]
        N5[Router retries or uses previously leased IP]
        N6[Internet access fails if retries fail]
    end

    B --> N1
    H --> N4
