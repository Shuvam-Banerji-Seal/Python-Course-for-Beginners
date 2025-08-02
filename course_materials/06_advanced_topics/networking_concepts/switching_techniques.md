
## 1. 📦 Packet Switching

```mermaid
flowchart LR
    A[Sender Device] --> B[Packet 1]
    A --> C[Packet 2]
    A --> D[Packet 3]
    
    B --> R1[Router A]
    C --> R2[Router B]
    D --> R3[Router C]

    R1 --> R4[Router D]
    R2 --> R4
    R3 --> R4

    R4 --> Z[Receiver Device]

    classDef packet fill:#ccf,stroke:#333;
    class B,C,D packet;
```

### 📘 Explanation:

* Data is broken into small **packets**.
* Each packet can take a different **route** to the destination.
* Routers forward packets based on routing tables.
* Final device **reassembles** the packets in order.

---

## 2. 🧳 Encapsulation & Decapsulation

```mermaid
flowchart TD
    App[Application Data] --> PDU7[Layer 7: Add Application Header]
    PDU7 --> PDU6[Layer 6: Add Presentation Header]
    PDU6 --> PDU5[Layer 5: Add Session Header]
    PDU5 --> PDU4[Layer 4: Add Transport Header TCP/UDP]
    PDU4 --> PDU3[Layer 3: Add Network Header IP]
    PDU3 --> PDU2[Layer 2: Add Data Link Header/Footer MAC]
    PDU2 --> PDU1[Layer 1: Bits Sent over Physical Medium]

    PDU1 --> RX1[Receiver Layer 1: Physical Layer]
    RX1 --> RX2[Remove Link Layer]
    RX2 --> RX3[Remove Network Header]
    RX3 --> RX4[Remove Transport Header]
    RX4 --> RX5[Remove Session/Presentation/Application Headers]
    RX5 --> Output[Original Application Data Reconstructed]

    classDef pdu fill:#cfc,stroke:#333;
    class PDU7,PDU6,PDU5,PDU4,PDU3,PDU2,PDU1 pdu;
```

### 📘 Explanation:

* Each layer **adds its own header** to the data = **Encapsulation**.
* Receiver removes headers in reverse = **Decapsulation**.
* Happens in both OSI and TCP/IP models.

---

## 3. 📡 Routers and Routing Tables

```mermaid
graph TD
    A[Router] --> TBL[Routing Table]
    TBL --> Entry1[Destination: 192.168.1.0/24 → Interface: eth0]
    TBL --> Entry2[Destination: 10.0.0.0/8 → Interface: eth1]
    TBL --> Entry3[Destination: 0.0.0.0/0 Default → Next-hop: ISP Router]

    A --> Pkt[Incoming Packet Dest: 10.0.3.4]
    Pkt --> Lookup[Router looks up destination in routing table]
    Lookup --> FWD[Forward Packet to Interface eth1]
```

### 📘 Explanation:

* Each router has a **routing table**.
* It maps destination networks to the correct **interface** or **next-hop**.
* Default route (`0.0.0.0/0`) is used for all unknown destinations (i.e., internet).

---

## 4. 🧭 Routing Protocols: RIP, OSPF, BGP

```mermaid
flowchart TB
    subgraph RIP [Routing Information Protocol RIP]
        RIP1[Uses Distance Vector]
        RIP2[Updates every 30 seconds]
        RIP3[Max hops: 15]
    end

    subgraph OSPF [Open Shortest Path First]
        OSPF1[Uses Link-State]
        OSPF2[Knows full network map]
        OSPF3[Fast convergence]
    end

    subgraph BGP [Border Gateway Protocol]
        BGP1[Used between ISPs]
        BGP2[Path Vector Protocol]
        BGP3[Used on internet backbone]
    end

    RIP -->|Intra-domain| RouterA
    OSPF -->|Intra-domain| RouterB
    BGP -->|Inter-domain| RouterC
```

### 📘 Explanation:

| Protocol | Type            | Use Case            | Metric Used      | Notes             |
| -------- | --------------- | ------------------- | ---------------- | ----------------- |
| RIP      | Distance Vector | Small networks      | Hop count        | Simple, slow      |
| OSPF     | Link-State      | Enterprise networks | Cost (bandwidth) | Fast convergence  |
| BGP      | Path Vector     | Internet-level      | Policy, path     | Used between ASes |

---

## ✅ Summary Visual Flow

```mermaid
flowchart LR
    Send[Sending Device] --> Encap[Encapsulation]
    Encap --> R1[Router 1]
    R1 --> R2[Router 2]
    R2 --> R3[Router 3]
    R3 --> Decap[Decapsulation]
    Decap --> Recv[Receiving Device]

    R1 -->|Uses| Table1[Routing Table]
    R2 -->|Uses| Table2[Routing Table]
    R3 -->|Uses| Table3[Routing Table]

    Table1 -->|Built by| Proto1[RIP or OSPF]
    Table3 -->|Built by| Proto2[BGP]
```










```mermaid
flowchart TD
    %% Title clusters
    subgraph Circuit_Switching["Circuit Switching"]
        direction TB
        CS1[Dedicated Communication Path Established]
        CS2[Resources Reserved for Entire Call Duration]
        CS3[Continuous Connection During Session]
        CS4[Exclusive Use of Circuit by Parties]
        CS5[Call Terminated and Resources Freed]
        
        CS_Advantages[Advantages:]
        CS_Adv1[Predictable Quality of Service]
        CS_Adv2[Low Latency Real Time Communication]
        CS_Adv3[Simple and Deterministic]
        
        CS_Disadvantages[Disadvantages:]
        CS_Dis1[Inefficient Resource Usage When Idle]
        CS_Dis2[Limited Flexibility and Adaptation]
    end

    subgraph Packet_Switching["Packet Switching"]
        direction TB
        PS1[Data Divided into Small Packets]
        PS2[Each Packet Has Header with Routing Info]
        PS3[Store and Forward at Each Router]
        PS4[Packets Share Network Resources Dynamically]
        PS5[Routing Decisions Made at Each Router]
        PS6[Packets May Take Different Routes]
        PS7[Packets Reassembled at Destination]
        PS8[Handles Packet Loss and Retransmission]

        PS_Advantages[Advantages:]
        PS_Adv1[Efficient Use of Bandwidth]
        PS_Adv2[Scalable and Flexible Network]
        PS_Adv3[Resilient to Network Failures]
        PS_Adv4[Supports Diverse Data Types]

        PS_Disadvantages[Disadvantages:]
        PS_Dis1[Variable Latency Due to Network Conditions]
        PS_Dis2[Packets May Arrive Out of Order]
    end

    %% Comparison nodes
    subgraph Comparison["Key Differences"]
        direction LR
        C1[Dedicated vs Shared Path]
        C2[Resource Reservation vs Dynamic Sharing]
        C3[Continuous Connection vs Packetized Data]
        C4[Low Delay but Inefficient vs Variable Delay but Efficient]
        C5[Simple Routing vs Complex Routing]
        C6[Less Adaptive vs Highly Adaptive]
    end

    %% Connections within circuit switching
    CS1 --> CS2 --> CS3 --> CS4 --> CS5
    CS_Advantages --> CS_Adv1
    CS_Advantages --> CS_Adv2
    CS_Advantages --> CS_Adv3
    CS_Disadvantages --> CS_Dis1
    CS_Disadvantages --> CS_Dis2

    %% Connections within packet switching
    PS1 --> PS2 --> PS3 --> PS4 --> PS5 --> PS6 --> PS7 --> PS8
    PS_Advantages --> PS_Adv1
    PS_Advantages --> PS_Adv2
    PS_Advantages --> PS_Adv3
    PS_Advantages --> PS_Adv4
    PS_Disadvantages --> PS_Dis1
    PS_Disadvantages --> PS_Dis2

    %% Comparison connections
    Circuit_Switching --- C1 --- Packet_Switching
    Circuit_Switching --- C2 --- Packet_Switching
    Circuit_Switching --- C3 --- Packet_Switching
    Circuit_Switching --- C4 --- Packet_Switching
    Circuit_Switching --- C5 --- Packet_Switching
    Circuit_Switching --- C6 --- Packet_Switching

    %% Style for groups
    classDef box fill:#fefefe,stroke:#222,stroke-width:1px,rounded-corners;
    %%class Circuit_Switching,Packet_Switching,Comparison box;
```