# 🚀 Project: Real-Time Vision AI for Robotics on Edge

> Inspired by: **[Optimize Performance of Vision AI Models on the Edge](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-s81833/)** (S81833, GTC 2026)

---

## Problem Statement

Deploy a multi-modal Vision Language Model (VLM) and stereo depth estimation pipeline on an NVIDIA Jetson device for a mobile robot that can:
1. **See** — process stereo camera feeds in real-time
2. **Understand** — use a VLM to answer natural language queries about the scene
3. **Navigate** — generate depth maps for obstacle avoidance

The challenge: doing all of this under **15W power budget** with **<100ms latency**.

---

## What You'll Build

A **"Robot Scene Inspector"** — a Jetson-powered robot companion that rolls around a space (warehouse, lab, home) and answers questions like:
- *"Is there anything blocking the hallway?"*
- *"How far away is that box?"*
- *"What safety hazards do you see?"*

---

## Architecture

```
┌─────────────┐     ┌──────────────────┐     ┌────────────────┐
│ Stereo Cam   │────▶│ Depth Estimation  │────▶│ Obstacle Map   │
│ (ZED 2i)     │     │ (Optimized INT8)  │     │ (Nav Stack)    │
└─────────────┘     └──────────────────┘     └────────────────┘
       │
       ▼
┌──────────────────┐     ┌────────────────┐
│ VLM (Cosmos/     │────▶│ Natural Lang.  │
│ Florence-2)      │     │ Response       │
│ Quantized FP16   │     │ via Speaker/UI │
└──────────────────┘     └────────────────┘
```

---

## Key Techniques from the Talk

These are the specific optimization strategies covered in S81833 that you'd apply:

### 1. VLM Multi-Modal Alignment Preservation
- **Problem:** Naively quantizing a VLM breaks the vision-language alignment
- **Solution:** Use alignment-aware quantization — freeze the projection layer, quantize vision encoder and LLM backbone separately
- **Your application:** Shrink Florence-2 or Cosmos Reason to FP16/INT8 while keeping visual Q&A accuracy

### 2. Stereo Depth Optimization for Real-Time
- **Problem:** Stereo depth models (e.g., RAFT-Stereo) are too slow for edge
- **Solution:** TensorRT optimization + temporal caching (reuse depth from previous frame for static regions)
- **Your application:** Run depth estimation at 30 FPS on Jetson Orin with <50ms latency

### 3. Power-Aware Model Scheduling
- **Problem:** Running VLM + depth simultaneously exceeds power budget
- **Solution:** Interleave inference — depth runs every frame, VLM runs on-demand (triggered by voice query)
- **Your application:** Stay within 15W by scheduling GPU workloads intelligently

---

## Hardware & Software

| Component | Choice |
|---|---|
| **Compute** | NVIDIA Jetson Orin Nano / AGX Orin |
| **Camera** | ZED 2i Stereo Camera or OAK-D |
| **Framework** | NVIDIA DeepStream + TensorRT |
| **VLM** | Florence-2 (quantized) or Cosmos Reason (if available) |
| **Depth** | RAFT-Stereo or SGM via NVIDIA VPI |
| **Language** | Python + C++ (DeepStream plugins) |
| **Nav (optional)** | ROS 2 + Nav2 |

---

## Implementation Phases

### Phase 1: Baseline (Week 1-2)
- [ ] Set up Jetson Orin with JetPack 6
- [ ] Run Florence-2 / Cosmos Reason unoptimized — measure baseline latency & power
- [ ] Run stereo depth model unoptimized — measure FPS

### Phase 2: Optimize VLM (Week 3-4)
- [ ] Export VLM to ONNX
- [ ] Apply alignment-aware quantization (FP16 backbone, keep projection layer FP32)
- [ ] Convert to TensorRT engine
- [ ] Benchmark: target <2s for visual Q&A response

### Phase 3: Optimize Depth (Week 4-5)
- [ ] Convert depth model to TensorRT INT8
- [ ] Implement temporal caching for static regions
- [ ] Benchmark: target 30 FPS, <50ms latency

### Phase 4: Integrate & Schedule (Week 6)
- [ ] Build power-aware scheduler: depth always-on, VLM on-demand
- [ ] Add voice trigger (whisper.cpp on Jetson) for hands-free queries
- [ ] End-to-end demo: robot navigates + answers questions

### Phase 5: Polish (Week 7-8)
- [ ] Web dashboard showing live depth map + VLM responses
- [ ] Log all Q&A for later review
- [ ] Measure total power consumption, optimize to stay <15W

---

## Success Metrics

| Metric | Target |
|---|---|
| Depth FPS | ≥ 30 FPS |
| Depth latency | < 50ms |
| VLM response time | < 2 seconds |
| Power consumption | < 15W sustained |
| VLM accuracy vs. unoptimized | > 95% alignment score |

---

## Why This Project Matters

After attending [S81833](https://www.nvidia.com/gtc/session-catalog/sessions/gtc26-s81833/), you'll have the specific knowledge to:
1. **Immediately apply** multi-modal alignment-preserving quantization to any VLM
2. **Deploy** stereo vision in real-time on power-constrained robots
3. **Build a portfolio piece** that demonstrates edge AI optimization — a highly sought-after skill
4. **Extend it** to industrial inspection, warehouse robotics, or assistive technology

This project combines Computer Vision, VLMs, Edge Deployment, and Robotics — hitting all your top interest areas in one build.
