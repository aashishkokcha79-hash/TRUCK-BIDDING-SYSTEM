# Truck Bidding System Implementation Plan

This document outlines the architecture and implementation plan for building a truck bidding web application using Django, HTML, CSS, and JavaScript.

## User Review Required

> [!IMPORTANT]
> Since this is a completely new project, we need to decide on a few implementation details. Please review the "Open Questions" section below before we begin coding.

## App Architecture

We will create a single Django project named `bidding_system` and an app named `core`.

### Proposed Models

1. **`User` (Django Built-in)**: We'll extend this using a `UserProfile` model.
2. **`UserProfile`**:
   - `user` (OneToOne to Django User)
   - `user_type` (Choices: 'Customer', 'Transporter')
   - `contact_number` (String)
3. **`TransporterProfile`**:
   - `user` (OneToOne to Django User)
   - `transporter_name` (String)
   - `vehicle_number` (String)
   - `current_latitude` (Float, for simulated live location)
   - `current_longitude` (Float, for simulated live location)
4. **`Requirement`**:
   - `customer` (ForeignKey to User)
   - `source_city` (String)
   - `destination_city` (String)
   - `status` (Choices: 'Open', 'Assigned', 'Closed')
   - `created_at` (DateTime)
   - `winning_bid` (ForeignKey to 'Bid', null=True, blank=True)
5. **`Bid`**:
   - `requirement` (ForeignKey to Requirement)
   - `transporter` (ForeignKey to User)
   - `amount` (Decimal)
   - `created_at` (DateTime)

### Core Features & Views

1. **Authentication Flow (Sign Up / Log In)**: Users will register as either a "Customer" or "Transporter".
2. **Customer Dashboard**:
   - Form to post a new load requirement (Source -> Destination).
   - View their active requests.
   - For a given request, automatically select and display the lowest bid (or a button to manually accept the lowest bid).
   - Once a bid is accepted, display the winning Transporter's details (contact, vehicle number, transporter name, and simulated live location on a map).
3. **Transporter Dashboard**:
   - View all "Open" requirements posted by customers.
   - Submit a bid amount for any open requirement.
   - View their past bids and win status.

### Frontend Aesthetics

> [!TIP]
> The UI will use vanilla HTML, CSS, and JS but will be styled to be dynamic, modern, and highly responsive. We will use sleek dark mode aesthetics, glassmorphism containers, smooth modern fonts (e.g., Inter), and interactive micro-animations to make it feel premium. 

## Proposed Changes (Phases)

### Phase 1: Project Setup and Models
- Initialize the Django project `bidding_system`.
- Create the `core` app.
- Define models and apply migrations.

### Phase 2: Authentication
- Create registration, login, and logout views.
- Build premium-looking login/signup forms.

### Phase 3: Core Features (Customer & Transporter)
- Create URLs, Views, and Templates for Customer Dashboard.
- Create URLs, Views, and Templates for Transporter Dashboard.
- Setup forms for creating requirements and submitting bids.

### Phase 4: Winner Selection & Simulation 
- Implement logic to automatically or manually choose the lowest bid.
- Create the "Winning Transporter Info" view using a dummy JS map integration (or simple coordinate simulation) for "Live Location".

## Open Questions

> [!WARNING]
> Please confirm the following points:
> 1. Do you want the system to **automatically** pick the lowest bid when a timer expires, or should the customer **manually** click "Accept Lowest Bid" to choose the winner? 
> 2. For the "Live Location", we can simulate this with dummy latitude/longitude changes on the frontend using JS and a simple OpenStreetMap embed. Is this acceptable?
> 3. Does the Transporter need to update their live location manually, or should we simulate it for demonstration purposes?

## Verification Plan

### Automated/Manual Testing
- Create a test Customer user and a test Transporter user.
- Customer posts a job.
- Transporter views the job and places a competitive bid on the Transporter dashboard.
- Customer reviews the bids, the system identifies the lowest, and the Transporter is awarded the job.
- Customer can view the exact details of the transporter and see the simulated live location.
