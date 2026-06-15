# Application Instrumentation & Security Event Logging Guide

- [Application Instrumentation \& Security Event Logging Guide](#application-instrumentation--security-event-logging-guide)
  - [Introduction](#introduction)
  - [Architecture Overview](#architecture-overview)
    - [Security Design](#security-design)
  - [Prerequisites](#prerequisites)
  - [Logger Implementation](#logger-implementation)
  - [Integration Example](#integration-example)
  - [Error Logging Middleware](#error-logging-middleware)
  - [Security Event Logging (SOC Use Cases)](#security-event-logging-soc-use-cases)
  - [Log Schema](#log-schema)
  - [MongoDB Setup](#mongodb-setup)
  - [Environment Configuration](#environment-configuration)
  - [ShieldEye Platform Usage](#shieldeye-platform-usage)
    - [Analysis \& Usage](#analysis--usage)
  - [Best Practices](#best-practices)
  - [Important Notes](#important-notes)
  - [Security Guidelines](#security-guidelines)
    - [Common Mistakes](#common-mistakes)

## Introduction

ShieldEye Log Analyzer is a security-focused log collection and analysis platform designed for developers and SOC analysts.

It enables applications to:

- Generate structured security and operational logs
- Store logs in MongoDB
- Detect anomalies and threats via ShieldEye analysis

## Architecture Overview

Application → Logger Middleware → MongoDB → ShieldEye → Analysis Engine

### Security Design

- Logs remain in your infrastructure (MongoDB)
- ShieldEye connects using a read-only account
- Prevents:
  - Log tampering
  - Unauthorized modification
  - Data exfiltration risks

## Prerequisites

Ensure the following are available:

- Node.js ≥ 18
- MongoDB Atlas (or self-hosted MongoDB)
- Express.js application
- Environment variables configured

## Logger Implementation

Create a centralized logging middleware:

```js
// middleware/shieldeye-logger.js
import { v4 as uuidv4 } from "uuid"
import clientPromise from "../config/db.js"

const client = await clientPromise
const db = client.db("logs")

export async function logEvent(req, res, {
    event_type,
    level = "info",
    category,
    source,
    message,
    stack = "",
    tags = []
}) {
    try {
        const collection = db.collection("event_logs")

        const log = {
            _id: uuidv4(),
            timestamp: new Date(),
            level,
            category,
            event_type,
            source,
            message,
            stack,
            app: {
                name: process.env.APP_NAME || "MyApp",
                version: process.env.APP_VERSION || "1.0.0"
            },
            user: {
                id: req?.validatedUserId || "anonymous",
                ip: req?.ip,
                method: req?.method,
                endpoint: req?.originalUrl,
                status: res?.statusCode,
                user_agent: req?.headers["user-agent"]
            },
            tags
        }

        await collection.insertOne(log)

    } catch (err) {
        // Fail-safe: logging failure must not break app
        console.error("ShieldEye Logger Error:", err.message)
    }
}

export function errorEvent(err, req, res, next) {
    logEvent(req, res, {
        event_type: err.name || "UnhandledException",
        level: "error",
        category: "server",
        source: req.originalUrl,
        message: err.message,
        stack: err.stack,
        tags: ["error", "exception"]
    })

    next(err)
}
```

## Integration Example

Controller Instrumentation

```js
import { logEvent } from "../middleware/shieldeye-logger.js"

export const createNote = async (req, res) => {
    const { user, title, text } = req.body

    if (!user || !title || !text) {
        return res.status(400).json({ message: "All fields required" })
    }

    const note = await Note.create({ user, title, text })

//  ==============================================================
//  Create log event when user created a note
//  ==============================================================
    if (note) {
        await logEvent(req, res, {
            event_type: "NOTE_CREATED",
            category: "application",
            source: "notesController",
            message: `User ${user} created a note`,
            tags: ["note", "creation"]
        })

        return res.status(201).json({ message: "Note created" })
    }

//  ==============================================================
//  Create log event when note creation failed
//  ==============================================================
    await logEvent(req, res, {
        event_type: "NOTE_CREATION_FAILED",
        level: "warn",
        category: "application",
        source: "notesController",
        message: "Note creation failed",
        tags: ["error"]
    })

    return res.status(400).json({ message: "Failed" })
}
```

## Error Logging Middleware

```js
import express from "express"
import { errorEvent } from "./middleware/shieldeye-logger.js"

const app = express()

// other middleware...

//  ==============================================================
//  Create log event when an error occurred
//  ==============================================================
app.use(errorEvent)
```

## Security Event Logging (SOC Use Cases)

Failed Login Attempt

```js
await logEvent(req, res, {
    event_type: "LOGIN_FAILED",
    level: "warn",
    category: "authentication",
    source: "authController",
    message: `Failed login attempt for ${req.body.username}`,
    tags: ["auth", "failed_login"]
})
```

Brute Force Detection Trigger

```js
await logEvent(req, res, {
    event_type: "MULTIPLE_FAILED_LOGINS",
    level: "critical",
    category: "security",
    message: "Possible brute force detected",
    tags: ["attack", "bruteforce"]
})
```

## Log Schema

| Field           | Type   | Description                  |
| --------------- | ------ | ---------------------------- |
| `_id`           | UUID   | Unique event ID              |
| `timestamp`     | Date   | Event time                   |
| `level`         | String | info, warn, error, critical  |
| `category`      | String | authentication, system, etc. |
| `event_type`    | String | Specific event name          |
| `message`       | String | Human-readable description   |
| `user.ip`       | String | Source IP                    |
| `user.endpoint` | String | API endpoint                 |
| `tags`          | Array  | Searchable labels            |

## MongoDB Setup

Visit [https://account.mongodb.com/account/login](https://account.mongodb.com/account/login) to create an account or login.

- Create database: `logs`
- Create collection: `event_logs`

Users

- Admin User
  - Role: `readWrite` on `logs`

- ShieldEye Agent
  - Username: `shieldeye_agent`
  - Role: `read` on `logs.event_logs`

## Environment Configuration

```env
MONGODBURI=mongodb+srv://<admin_username>:<strong_password>@...
```

## ShieldEye Platform Usage

Visit [ShieldEye web](https://shieldeye.holoolagoke.com), create an account and login to your profile. Goto the preference page, fill the require fieldd:

Required fields:

- **mongoUrl**: mongodb+srv://shieldeye_agent:<strong_password>@...
- **level**: an array of log levels to monitor when creating alerts. Example:

### Analysis & Usage

Logs are collected directly from the user’s MongoDB instance. ShieldEye analyzes logs for anomalies and security patterns

Logs can be filtered by:

- event_type
- level
- category
- tags
- Date
- Word search

Regular review is recommended to detect abnormal behavior early

## Best Practices

- Use clear and descriptive message values
- Apply consistent category naming
- Use lowercase tags for consistency
- Avoid logging sensitive data (passwords, tokens, secrets, PII)
- Archive or rotate old logs to prevent database bloat

## Important Notes

- Logs are not stored on ShieldEye servers. If logs are deleted from your MongoDB instance, they cannot be recovered.
- Only provide MongoDB URLs created with the shieldeye_agent read-only user.
- ShieldEye web vaersion analyzes logs generated within the current calendar month only (Day 1 – Day 31), at the start of each new month, ShieldEye begins analysis on newly generated logs.
- Investigation of historical logs beyond the current month is not supported in the web version.
- Investigators or developers are encouraged to jot down unusual patterns or export their logs from MongoDB if they want to preserve historical data for offline analysis.
- A desktop version of ShieldEye is available and supports long-term log retention and historical forensic analysis.
- Since logs are stored in the user’s MongoDB instance, they can be exported and uploaded into the ShieldEye Desktop application.
- The desktop version enables investigations beyond the current month without impacting web platform performance.

## Security Guidelines

Never log:

- Passwords
- Authentication tokens (JWT)
- API keys
- Personally Identifiable Information (PII)

Logging sensitive data can lead to:

- Data breaches
- Compliance violations

### Common Mistakes

- Not awaiting `logEvent` (logs may not persist)
- Logging too much data (causes noise)
- Inconsistent category naming
- Logging sensitive data
- Not monitoring logs regularly
