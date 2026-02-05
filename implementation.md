# TrashCollector AI

### Vision-Based Waste Classification for Smart Waste Segregation

---

## 1. Overview

**TrashCollector AI** is an AI-powered waste identification system designed to classify trash items from images and recommend the correct segregation category (e.g., wet, dry, recyclable, hazardous, e-waste). The system uses **on-device vision-language models via Ollama**, enabling privacy-friendly, offline-capable, and low-latency inference.

The primary goal is to improve waste segregation accuracy by reducing human error and lack of awareness through simple visual interaction.

---

## 2. Problem Statement

* Poor waste segregation due to lack of awareness
* Improper disposal of recyclable and hazardous materials
* Health, environmental, and financial consequences
* Existing systems rely heavily on manual sorting

**TrashCollector AI** solves this by using computer vision + language understanding to classify waste instantly from a photo.

---

## 3. System Objectives

* Accept an image of an object as input
* Identify the object using a vision-language model
* Classify it into a predefined waste category
* Provide clear segregation instructions
* Run locally using Ollama (no cloud dependency)
* Be UI-friendly for mobile, web, and kiosk setups

---

## 4. High-Level Architecture

```
[Camera / Image Upload]
          ↓
[Frontend UI]
          ↓
[Inference API Layer]
          ↓
[Ollama Vision Model]
          ↓
[Waste Classification Logic]
          ↓
[Result + Segregation Guidance]
```

---

## 5. Model Selection (Ollama – Vision Models)

### Recommended Vision-Language Models

#### Primary Choice

**Qwen3-VL (Vision-Language Model)**

* Latest Qwen vision model with improved object grounding
* Better fine-grained classification for everyday objects
* Strong multimodal reasoning (image + text)
* Optimized for local inference with Ollama

**Suggested Variants:**

* `qwen3-vl:7b` – recommended default (accuracy vs speed balance)
* `qwen3-vl:3b` – edge / low-resource systems

#### Secondary Choice (Stable)

**Qwen2.5-VL**

* Proven stability
* Slightly lower accuracy than Qwen3-VL
* Good fallback model

#### Lightweight Alternatives

| Model     | Use Case                     |
| --------- | ---------------------------- |
| LLaVA 1.6 | General-purpose vision tasks |
| BakLLaVA  | Embedded / low-RAM devices   |

**Why Qwen VL Family:**

* Trained on real-world objects
* Clear natural language responses
* Strong compatibility with Ollama
* Suitable for offline-first systems

-----|--------|
| LLaVA 1.6 | Good general vision tasks |
| BakLLaVA | Lightweight deployments |
| Qwen2-VL | Stable fallback option |

**Why Qwen VL:**

* Better visual grounding
* Clear natural language outputs
* Works reliably with Ollama

---

## 6. Waste Classification Schema

The model output is post-processed into fixed categories:

| Category  | Examples                 |
| --------- | ------------------------ |
| Wet Waste | Food scraps, fruit peels |
| Dry Waste | Paper, cardboard         |
| Plastic   | Bottles, wrappers        |
| Metal     | Cans, foil               |
| Glass     | Bottles, jars            |
| E-Waste   | Batteries, chargers      |
| Hazardous | Medical waste, chemicals |
| Unknown   | Unclear or mixed items   |

---

## 7. Prompt Engineering Strategy

### Vision Prompt Template

```
You are a waste segregation assistant.

Analyze the image and:
1. Identify the object
2. Classify it into one waste category
3. Respond in JSON format

Allowed categories:
Wet, Dry, Plastic, Metal, Glass, E-Waste, Hazardous, Unknown

Respond only in JSON.
```

### Example Output

```json
{
  "object": "Plastic water bottle",
  "category": "Plastic",
  "confidence": "High",
  "instruction": "Dispose in plastic recycling bin"
}
```

---

## 8. Backend (Inference Layer)

### Responsibilities

* Accept image from UI
* Forward image + prompt to Ollama
* Parse model response
* Validate category
* Send clean JSON to frontend

### Suggested Stack

* Python (FastAPI) or Node.js (Express)
* Ollama local server
* JSON-based API

---

## 9. UI/UX Design Guidelines

### Design Principles

* Minimalist
* Fast interaction (< 3 steps)
* High readability
* Works on mobile, web, and kiosks

### Core UI Flow

```
Capture / Upload Image → Analyze → Result
```

### UI Screens

#### 1. Capture Screen

* Live camera view or upload option
* Single object guidance overlay
* "Capture" CTA

#### 2. Processing State

* Loading indicator
* Text: "Identifying waste type…"

#### 3. Result Screen

* Detected object name
* Waste category (large, bold)
* Disposal instruction
* Confidence level

### Category Color Coding

| Category  | UI Color |
| --------- | -------- |
| Wet Waste | Green    |
| Dry Waste | Blue     |
| Plastic   | Yellow   |
| Metal     | Gray     |
| Glass     | Teal     |
| E-Waste   | Purple   |
| Hazardous | Red      |
| Unknown   | Neutral  |

### Accessibility

* Large fonts
* Icon + text indicators
* Color + label redundancy

-------|------|
| Wet | Green |
| Dry | Blue |
| Plastic | Yellow |
| Metal | Gray |
| Glass | Teal |
| E-Waste | Purple |
| Hazardous | Red |

---

## 10. Error Handling

* Blurry image → ask user to retake
* Multiple objects → request single item
* Low confidence → return `Unknown`

---

## 11. Performance Considerations

* Resize images before inference
* Cache common results
* Use smaller model for edge devices
* Batch inference for kiosks

---

## 12. Security & Privacy

* No image storage by default
* All inference runs locally
* Optional anonymized logs

---

## 13. Future Enhancements (Optional)

* Multi-object detection
* Region-based segmentation
* Local language output (Tamil, Hindi, etc.)
* Integration with smart bins

---

## 14. Summary

TrashCollector AI combines **vision-language AI + local inference** to create a scalable, privacy-first waste segregation system. Using **Qwen VL models via Ollama**, the system achieves accurate classification while remaining lightweight and deployment-friendly.

---

**Document Version:** 1.0
**Prepared for:** TrashCollector AI Engineering Team
