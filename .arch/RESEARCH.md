# target employer (target employer) - Research Notes

## 1. Company Overview

- **Full name**: target employer, Inc.
- **Founded**: 2018 (some sources say 2017)
- **HQ**: Boston, MA
- **Other offices**: Washington D.C., Denver, Gdansk (Poland)
- **Founders**: Phillip Buckendorf (CEO), Kris Dorosz (CTO, PhD in CS from AGH), Lucas Kukielka
- **Employees**: ~130
- **Revenue**: ~$29.3M
- **Funding**: Series B ($34M led by Andreessen Horowitz); Series A ($22M). Investors include Bloomberg Beta, Spark Capital, Renegade Partners, Gradient Ventures
- **Recognized** in a16z's American Dynamism 50 AI edition

---

## 2. Products

### domain platform Platform (core product)
An AI-enabled platform for mission-critical operations. Six modules:

1. **Data Fusion** - Ingests 100+ pre-integrated geospatial/OSINT data sources (ADS-B, AIS, FAA SWIM, CoSPA, weather). Open data architecture for legacy system integration.
2. **Domain Modeling** - Creates a 4D digital twin of operating environments (3 spatial dims + time) across air, land, sea.
3. **Prediction** - ML-powered lookahead simulations of future operating environment state.
4. **Optimization** - Continuously evaluates alternative courses of action; generates optimized recommendations.
5. **Communications** - Secure peer-to-peer and enterprise collaboration (air-to-ground integration).
6. **Replay & Analytics** - Logs every geospatial/temporal event for retrospective analysis, training, and compliance.

### Flyways AI (commercial aviation product, built on domain platform)
- Flow management platform for air traffic and airline operations
- Optimizes routes by analyzing weather, winds, turbulence, airspace constraints, traffic volume
- Deployed at Alaska Airlines for 4+ years
- Results: optimization opportunities on 55% of flights; 3-5% fuel savings on flights >4 hrs; saved 1.2M gallons of fuel in one year (11,958 metric tons CO2)
- 22% improvement in air traffic prediction accuracy

### Defense Applications
- Multi-domain (space, air, land, sea) situational awareness
- "Logistics Kill Chain" concept: applying military kill-chain doctrine to logistics optimization at machine speed
- Supports OODA loop acceleration with continuous 4D lookahead
- Predicts kinetic and non-kinetic risks
- Edge/mobile capabilities for tactical deployment
- Security compliance: SOC II Type II, DoD SRG IL4-IL6, NIST 800-171, CMMC L2

### Other Verticals
- Freight logistics, rail, maritime transportation, energy

---

## 3. Tech Stack

### Backend / Core
| Technology | Source |
|---|---|
| **Rust** | Software Engineer job posting (explicitly listed) |
| **Python 3** | Multiple job postings (SWE, Full Stack, Cloud Platform, ML Engineer) |
| **PostgreSQL** | Cloud Platform Engineer job posting |
| **AWS** | Multiple postings |
| **Kubernetes** | Multiple postings |
| **Docker** | Multiple postings |
| **Terraform** | Multiple postings |
| **Helm** | Cloud Platform Engineer posting |
| **Grafana / Prometheus / Graphite** | Cloud Platform Engineer posting (monitoring) |

### Frontend
| Technology | Source |
|---|---|
| **TypeScript** | Full Stack & Frontend Engineer postings |
| **React** | Full Stack & Frontend Engineer postings |
| **Redux** | Full Stack Engineer posting |
| **Mapbox / Maplibre** | Full Stack & Frontend Engineer postings |
| **Firebase** | Frontend Engineer posting |
| **WebGL / WebGPU / ThreeJS** | Frontend Engineer posting |
| **WebAssembly (WASM)** | Frontend Engineer posting |
| **React Native** | Frontend Engineer posting |

### ML / AI
| Technology | Source |
|---|---|
| **TensorFlow / PyTorch / scikit-learn** | ML Engineer posting |
| **Apache Beam** | ML Engineer posting (data pipelines) |
| **MLflow** | ML Engineer posting (experiment tracking) |
| **LangChain** | ML Engineer posting (LLM frameworks) |
| **RAG systems** | ML Engineer posting |
| **Transformer architectures** | ML Engineer posting |

### Key Themes
- Heavy geospatial focus (Mapbox, 4D modeling, real-time rendering)
- Real-time data streaming (100+ data feeds)
- ML/AI at the core (prediction, optimization, simulation)
- Cloud-native (K8s, Docker, AWS, Terraform)
- Strong emphasis on LLM integration in development workflows
- Security clearance required (U.S. clearance eligible or holding)

---

## 4. Engineering Culture & Job Requirements

### Full Stack Engineer (Boston)
- **Languages**: Python, JavaScript, TypeScript
- **Frontend**: React, Redux, Mapbox, TypeScript
- **Infra**: AWS, Kubernetes, Docker, Terraform
- **Must**: Proficient with modern LLM tools for development acceleration
- **Must**: Eligible for U.S. security clearance
- **Must**: Willing to travel

### Software Engineer (Boston)
- **Languages**: Rust and Python (explicitly stated)
- **Focus**: Building 0-to-1 products and scaling 1-to-n
- **Must**: Foundation to learn Rust and Python quickly
- **Must**: Security clearance eligible

### Frontend Engineer (Boston & Poland)
- **Languages**: JavaScript/TypeScript
- **Frameworks**: React, React Native, Redux, Mapbox/Maplibre
- **Graphics**: WebGL, WebGPU, ThreeJS
- **Performance**: WebAssembly (WASM)
- **Focus**: Real-time rendering of high-density geospatial data on map-based apps

### Machine Learning Engineer (Boston & Poland)
- **Languages**: Python
- **Frameworks**: TensorFlow, PyTorch, scikit-learn
- **Production ML**: Apache Beam, MLflow, data versioning, model governance
- **LLMs**: Prompt engineering, fine-tuning, RAG, LangChain
- **Architectures**: Transformers, classical ML, deep learning
- **Practices**: Experiment tracking, automated testing pipelines

### Cloud Platform Engineer (Boston & Poland)
- **Stack**: Kubernetes, Docker, AWS, PostgreSQL, Helm, Terraform, Python 3
- **Monitoring**: Grafana, Prometheus, Graphite
- **Goal**: Scale infrastructure to 10x current load for mission-critical flight ops

### Staff Engineer (Boston & Poland)
- Lead technical challenges, architect solutions, mentor engineers
- Salary range: $124K-$199K base (Glassdoor estimate)

---

## 5. Interview Process

### Structure
1. **Pre-screen call** with recruiter
2. **HackerRank assessment** (online coding)
3. **Two 1-hour deep-dive coding sessions** (one frontend, one backend)
4. **Technical onsite** (4-6 hours)
- Total timeline: ~4 weeks

### What to Expect
- **Coding**: LeetCode medium to medium-hard difficulty
- **System Design**: E.g., "Design a system architecture for an API providing flight status gathered from multiple sources"
- **Platforms used**: Zoom, Google Meet, HackerRank, CodeSignal, CoderPad
- **Difficulty**: Described as "quite difficult" -- they're looking for "elite engineering talent"
- **Style**: FAANG-style interviews; interviewers are willing to work with candidates
- **Philosophy**: "An opportunity to simulate what it would be like working together"

### Candidate Feedback (Glassdoor)
- Mixed experiences: some report seamless process, others cite poor recruiter communication
- Some report interviewers looking for specific answers to open-ended questions
- Criticism: "FAANG-style interviews but with non-FAANG level compensation" (though equity could bridge gap)

---

## 6. Compensation

### Software Engineer (from InterviewCoder / Levels.fyi estimates)
| Level | Title | Total Comp (Median) | Base | Bonus | Equity | Exp |
|---|---|---|---|---|---|---|
| L3 | SWE II | $194K | $134-180K | $15-30K | $36-75K | 0-2 yr |
| L4 | SWE III | $283K | $150-210K | $20-40K | $75-150K | 2-5 yr |
| L5 | Senior SWE | $401K | $180-240K | $27-50K | $130-200K | 5-8 yr |

Note: these figures are estimates from InterviewCoder.co and may be aspirational. Levels.fyi reports median of $229K for SWE. Glassdoor Staff Engineer range is $124-199K base.

---

## 7. GitHub / Open Source Presence

- No official target employer GitHub organization found
- Individual employee: Piotr Mazur (Engineering Manager) has a GitHub profile (pitirus) with ML/aviation projects
- Company appears to keep code proprietary (defense/commercial sensitivity)

---

## 8. Glassdoor Reviews Summary

### Pros
- Strong team deeply invested in culture
- Seamless onboarding that gets you contributing quickly
- Chance to build at a small company with industry-changing potential
- Fantastic management, cool product
- Good benefits (AskHenry, premium healthcare, top hardware)
- Fast iteration, high-impact work

### Cons
- No real HR function; policies still being built
- Not for people uncomfortable with ambiguity
- Mixed recruiter experiences
- Some report compensation below FAANG despite similar interview difficulty
- Only 6 reviews total on Glassdoor (small sample)

---

## 9. Relevant Domain Algorithms & CS Concepts

### Graph & Search Algorithms
- **A* search** - Used in flight path optimization; heuristics based on wind fields and fuel cost
- **Dijkstra's algorithm** - Shortest path in airspace networks
- **D* / D* Lite** - Dynamic replanning as conditions change
- **Graph search on airspace networks** - Waypoints as nodes, airways as edges

### Optimization
- **Linear programming / Mixed-integer programming** - Route optimization with constraints (fuel, time, airspace restrictions)
- **Constraint satisfaction problems (CSP)** - Airspace deconfliction, scheduling
- **Multi-objective optimization** - Balancing fuel, time, safety, emissions simultaneously
- **Combinatorial optimization** - Fleet routing, gate assignment, crew scheduling

### Machine Learning
- **Reinforcement learning** - Traffic flow coordination, dynamic trajectory planning
- **Deep learning / Transformers** - 4D trajectory prediction, weather pattern forecasting
- **Time series forecasting** - Demand/capacity prediction, weather prediction
- **Anomaly detection** - Identifying irregular operations

### Geospatial
- **Spatial indexing** (R-trees, quad-trees, H3 hexagonal hierarchical index)
- **Great-circle distance / Haversine formula** - Earth-surface distance calculations
- **Coordinate reference systems** - WGS84, projections for map rendering
- **Geofencing** - Airspace boundary detection
- **Point-in-polygon** - Determining aircraft position relative to airspace sectors

### Real-Time Systems
- **Stream processing** - Ingesting 100+ data feeds (ADS-B positions, weather, SWIM)
- **Complex event processing** - Detecting meaningful patterns in real-time data streams
- **Pub/sub architectures** - Distributing real-time updates
- **WebSocket / Server-Sent Events** - Pushing updates to frontend map displays

### Simulation
- **Monte Carlo simulation** - Probabilistic trajectory prediction
- **Agent-based simulation** - Modeling individual aircraft behavior in airspace
- **Digital twin architectures** - 4D environment modeling
- **Discrete-event simulation** - Airport/airspace capacity modeling

### Data Structures
- **Priority queues / heaps** - For A*/Dijkstra path finding
- **Spatial data structures** - KD-trees, R-trees for nearest-neighbor queries on aircraft
- **Interval trees** - Time-based scheduling and conflict detection
- **Graphs** - Airway networks, constraint networks

---

## 10. Key Domains to Study

Based on the tech stack and product, focus areas for interview prep:

### Must-Know
1. **Python** - Core backend language; know it deeply
2. **Rust** - Explicitly required for SWE roles; study ownership, lifetimes, async
3. **TypeScript/React** - Frontend foundation; know hooks, state management, Redux
4. **System design** - Real-time data pipelines, geospatial APIs, streaming architectures
5. **LeetCode medium** - Graph problems, dynamic programming, string manipulation
6. **SQL / PostgreSQL** - Data modeling for geospatial and time-series data
7. **AWS / Kubernetes / Docker** - Cloud-native deployment and scaling

### Good-to-Know
1. **Mapbox / WebGL** - Map-based visualization, tile servers, vector tiles
2. **ML fundamentals** - Supervised/unsupervised learning, model serving, MLOps
3. **Graph algorithms** - Shortest path, A*, network flow
4. **Geospatial concepts** - Coordinate systems, spatial indexing, projections
5. **Real-time streaming** - Event-driven architecture, pub/sub

### Domain Knowledge
1. **Aviation basics** - METAR/TAF (weather), NOTAM, waypoints, airways, flight levels
2. **FAA SWIM** - System Wide Information Management data feeds
3. **ADS-B** - Automatic Dependent Surveillance-Broadcast (aircraft position data)
4. **Air traffic flow management** - Ground delay programs, miles-in-trail, reroutes
5. **4D trajectory** - 3D position + time for flight path optimization

---

## Sources

- [target employer Company Page](https://www.example.com/company)
- [target employer Careers](https://www.example.com/careers)
- [target employer domain platform Platform](https://www.example.com/platform)
- [target employer Air Traffic Management](https://www.example.com/solutions/air-traffic-management)
- [target employer Defense](https://www.example.com/solutions/defense)
- [Full Stack Engineer Job](https://jobs.ashbyhq.com/example.com/c97b6f01-a032-49dc-9ad1-c897912baab8)
- [Software Engineer Job](https://jobs.ashbyhq.com/example.com/6462d3d1-443c-4a5a-8667-c1d0472fa32d)
- [ML Engineer Job](https://jobs.ashbyhq.com/example.com/a035a6a4-0aee-4611-ae43-d0592995416a)
- [Cloud Platform Engineer Job](https://simplify.jobs/p/da5489a1-02c0-4b82-a546-8b1a6ee3967c/Cloud-Platform-Engineer)
- [All Open Positions](https://jobs.ashbyhq.com/example.com)
- [Glassdoor Reviews](https://www.glassdoor.com/Reviews/Air-Space-Intelligence-Reviews-E6407720.htm)
- [Glassdoor Interviews](https://www.glassdoor.com/Interview/Air-Space-Intelligence-Interview-Questions-E6407720.htm)
- [Levels.fyi Salaries](https://www.levels.fyi/companies/airspace-intelligence/salaries/software-engineer)
- [InterviewCoder Salary Guide](https://www.interviewcoder.co/software-engineer-salaries/airspace-intelligence-software-engineer-salary)
- [a16z Investment Announcement](https://a16z.com/announcement/investing-in-air-space-intelligence/)
- [Alaska Airlines Partnership](https://news.alaskaair.com/sustainability/how-ai-is-helping-alaska-airlines-plan-better-flight-routes-and-lower-emissions/)
- [Alaska Airlines Renewal](https://www.prnewswire.com/news-releases/alaska-airlines-renews-partnership-with-air-space-intelligence-solidifying-commitment-to-ai-powered-innovation--driving-fuel-efficiency-goals-302218646.html)
- [Startup Snapshot (Substack)](https://aaronpickard.substack.com/p/air-space-intelligence-a-startup)
- [Getlatka Revenue Data](https://getlatka.com/companies/example.com)
