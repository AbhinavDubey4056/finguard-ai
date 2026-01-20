🛡️ Finguard AI - Deepfake Edge Agent
Autonomous Edge AI System for Deepfake Detection & Forensic Analysis

Finguard AI is a secure, edge-optimized system designed to detect deepfakes in video and audio media. It combines a high-performance FastAPI backend for inference with a comprehensive Streamlit dashboard for forensic analysis, user management, and live security verification.

🚀 Key Features
Multi-Modal Analysis:

Video: Frame-by-frame analysis using Xception-based deep learning models, temporal aggregation, and face alignment.

Audio: Heuristic and signal-based analysis to detect synthetic voice artifacts.

Forensic Dashboard (UI):

Secure login portal with role-based access and cryptographic security integraion for admin login.

Upload interface for batch media analysis.

Detailed "Explanation Engine" reports (Verdict, Risk Level, Confidence Score).

🔴 Live Verification Portal:

Real-Time Biometric Broadcast: WebRTC-based secure streaming for live agent authentication(main integration will be with the tie ups)

Challenge-Response Protocol: Generates dynamic Session Codes that the user must speak to verify liveness.

Environment Fingerprinting: Detects the use of automation tools (e.g., Selenium/Webdrivers,Rooted Device, VM, Spyware) and validates hardware concurrency cores to prevent spoofing.

Autonomous Agent:

Decision Engine: Automatically determines verdicts (REAL vs. DEEPFAKE) based on confidence thresholds.

Integrity Checks: Verifies input media integrity before processing.

Project/
├── app/
│   ├── main.py                # FastAPI Backend Entry Point
│   ├── config.py              # System Configuration
│   └── ui/
│       ├── app.py             # Streamlit Frontend Dashboard
│       └── serviceAccountKey.json  # Firebase Credentials (Required)
├── agent/                     # Autonomous Logic
│   ├── decision_engine.py     # Verdict Logic
│   ├── explanation_engine.py  # Report Generation
│   └── policy_rules.py        # Threshold Policies
├── inference/                 # AI Inference Engine
│   ├── deepfake_infer.py      # Video Model Inference
│   ├── audio_infer.py         # Audio Analysis Logic
│   ├── model_loader.py        # PyTorch Model Management
│   └── temporal_aggregation.py # Frame-to-Video Score Aggregation
├── preprocessing/             # Media Pipeline
│   ├── video_loader.py        # Video I/O
│   ├── frame_sampler.py       # Frame Extraction
│   ├── face_detector.py       # Face Detection (OpenCV/MTCNN)
│   └── normalization.py       # Image Normalization
├── security/
│   ├── integrity_check.py     # File Security Verification
│   └── otp_utils.py           # Authentication Utilities
├── app_logging/               # System Logs
│   └── event_logger.py
└── requirements.txt           # Python Dependencies

🛠️ Installation & Setup
Prerequisites

Python 3.8+

Google Firebase Project (for Firestore)

1. Install Dependencies

Bash
pip install -r requirements.txt
Note: For the Live Portal, ensure streamlit-webrtc and streamlit-js-eval are installed.

2. Configure Firebase

To use the Dashboard and Audit Logging, you must add your Firebase credentials:

Generate a serviceAccountKey.json from your Firebase Console.

Place the file in Project/app/ui/serviceAccountKey.json.

3. Model Weights

Ensure your deep learning model weights (e.g., deepfake_model.pth) are placed in the models/ directory.

🚦 Usage
The system requires running the Backend (FastAPI) and Frontend (Streamlit) simultaneously.

Step 1: Start the Backend API

This handles the heavy lifting of video processing and inference.

Bash
# Run from the root directory
python -m app.main
Server will start at: http://localhost:8000

Step 2: Start the Forensic Dashboard

This launches the user interface.

Bash
streamlit run app/ui/app.py
UI will open at: http://localhost:8501

🔴 Live Verification Demo
The Live Mode is designed for secure, real-time agent verification.

Launch the Dashboard and log in (Default: admin / 1234).

Select "Live" from the navigation dropdown in the top right.

Grant Permissions: Allow the browser to access your webcam and microphone.

Verification Steps:

Biometric Broadcast: The WebRTC stream analyzes video/audio artifacts in real-time.

Session Code: A unique alphanumeric code (e.g., A7X92B) is displayed. The agent must speak this code into the camera.

Security Scan: Click the "Security Status" tab to view forensic metadata:

Hardware Cores: Validates device capabilities.

Webdriver Active: Checks for automated bot control.

Browser String: Verifies client identity.

🔌 API Endpoints
The FastAPI backend exposes the following endpoints:

Method	Endpoint	Description
GET	/health	Check system status and runtime mode.
POST	/analyze/video	Upload .mp4, .avi, .mov. Returns Deepfake Score & Verdict.
POST	/analyze/audio	Upload .wav, .mp3. Returns Audio Authenticity Score

🗄️ Database Architecture (Cloud Firestore)

The system connects to Firestore using the serviceAccountKey.json credentials. It operates in "Live Sync" mode, meaning changes made in the dashboard (like adding a user) are immediately reflected in the cloud database.

1. 🆔 SIC Code (Secure Identity Code)

The SIC Code is a unique identifier assigned to authorized "Users" (Admins/Personnel) in the system.

Generation Logic: It is a randomly generated 6-character alphanumeric string (A-Z, 0-9) created by the generate_sic() function.

Storage: Stored in the users collection.

Schema:

JSON
{
  "Name": "John Doe",
  "SIC": "A7X92B"  // Auto-generated unique key
}



Purpose: Acts as a secure, short-code credential for verifying authorized personnel access.

2. 👔 Employee Records

Different from "Users," employees are tracked with a standard corporate ID format.

Generation Logic: Uses generate_emp_id() to create a format like EMP + 3 random digits (e.g., EMP123).

Storage: Stored in the employees collection.

Schema:

JSON
{
  "Name": "Jane Smith",
  "ID": "EMP402"
}



3. 🔐 Encrypted Secrets Vault

A secure storage collection for sensitive keys or passwords.

Feature: The UI treats the Value input as a password field (masked), though it is currently stored as a string in the database.

Storage: Stored in the secrets collection.

Schema:

JSON
{
  "Key": "API_MASTER_KEY",
  "Value": "******" // Sensitive data
}


4. 📝 Audit Logs (Forensic Trail)

This is the most critical database feature for the Deepfake Agent. Every time a video or audio file is analyzed, an immutable report is automatically written to the database.

Generation: Triggered by the process_analysis function after inference.

Storage: Stored in the audit_reports collection.

Schema:

JSON
{
  "ReportID": "REP-XYZ123",        // Unique Report ID
  "Timestamp": "2025-10-27 14:30:00",
  "Filename": "suspect_video.mp4",
  "MediaType": "Video",
  "Verdict": "DEEPFAKE",           // Result from Agent
  "Confidence": "98.5%",           // Model Probability
  "RiskLevel": "CRITICAL",
  "Details": "Face artifacts detected..."
}



⚡ Live Synchronization Features

Streamed Updates: The dashboard uses db.collection(...).stream() to fetch the latest data, ensuring that if an admin adds a user from one device, it appears instantly on others.

State Management: The app uses Streamlit's session_state to cache this data temporarily to prevent excessive database reads during the session.


🔐 Cryptographic Security Architecture
Finguard AI employs a Zero-Trust Authentication approach, ensuring that sensitive access tokens are never stored in plain text.

1. SHA-256 Hashing Protocol
Located in: utils/otp_utils.py

The system utilizes industry-standard SHA-256 (Secure Hash Algorithm 256-bit) to secure ephemeral authentication tokens.

One-Way Encryption: One-Time Passwords (OTPs) generated for session validation are immediately hashed before verification. The raw OTP is never stored in the database, preventing reverse-engineering even in the event of a data breach.

Implementation:

Python
# OTPs are converted to a fixed 64-character hexadecimal signature
hashlib.sha256(otp.encode()).hexdigest()
2. Ephemeral Session Expiration
Located in: utils/otp_utils.py

To prevent "Replay Attacks" (where an attacker intercepts a valid code and tries to use it later), all cryptographic tokens have a strict time-to-live (TTL).

Expiry Window: 400 seconds (6.6 minutes).

Automatic Invalidation: The is_expired() utility validates the token's timestamp against the system clock at the moment of access. Any token older than the window is mathematically rejected, regardless of its correctness.

3. Secure Input Integrity
Located in: security/integrity_check.py

Beyond login, cryptographic security extends to the media pipeline.

File Hashing: Every uploaded video/audio file undergoes a cryptographic checksum verification (Input Integrity Check) to ensure the data has not been tampered with during transit before the AI processing begins.
