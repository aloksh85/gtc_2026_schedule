# Pre-GTC 2026 Reading & Concept List

Since you have professional ROS experience but are ramping up on LLMs, your goal before March 16th is to understand the vocabulary and architectural paradigms of Foundation Models. When you encounter these terms at GTC, you will be able to immediately map them to your robotics knowledge.

---

## 1. Core LLM Concepts (The "Brain" of the Robot)

*   **Transformers & Self-Attention:** The underlying architecture of modern LLMs. Understand how they process sequence data (like words, or even trajectory checkpoints).
*   **Tokens & Context Window:** LLMs process "tokens", not words. The "context window" is the maximum number of tokens it can hold in its working memory. *Robotics correlation: Think of the context window as your finite RAM for high-level state tracking.*
*   **Prompt Engineering & Few-Shot Learning:** How to talk to the model. *Robotics correlation: This is effectively "tuning the hyperparameters" of the behavioral heuristics.*
*   **RAG (Retrieval-Augmented Generation):** Giving the LLM a search engine across your internal data before it answers. *Robotics correlation: Looking up the building schematic or a manual before executing a path plan.*
*   **Agentic Frameworks (e.g., LangChain, AutoGen):** Systems that allow LLMs to use "tools" (like Python interpreters, search, or API calls). *Robotics correlation: Allowing an LLM to call `rclpy` to publish to a ROS topic.*

## 2. Multimodal and Vision-Language Models (VLMs) (The "Eyes")

*   **VLMs (e.g., LLaVA, NVIDIA VILA):** Models that process *both* text and images. You can pass a camera frame to a VLM and ask "Is the path clear?" or "Where is the red mug in pixel coordinates?"
*   **Semantic Scene Understanding:** Moving from bounding boxes (classic CV) to dense, conversational understanding of the environment.

## 3. NVIDIA-Specific Vocabulary to Learn
When at GTC, these frameworks are mentioned incessantly. Be familiar with what layer of the stack they occupy:

*   **TensorRT & TensorRT-LLM:** NVIDIA's optimization compiler. It shrinks (quantizes) massive LLMs so they run faster and use less VRAM, crucial for edge devices like Jetsons.
*   **Isaac ROS (NITROS):** Hardware-accelerated ROS 2 packages. NVIDIA optimizes classic perception nodes (stereo vision, VSLAM) to run natively on the Jetson GPU without CPU overhead.
*   **Metropolis:** NVIDIA's application framework for edge vision. Often used for stationary multi-sensor infrastructure that might communicate with mobile robots.
*   **Omniverse / Isaac Sim:** The simulation engine built on USD (Universal Scene Description). It is used massively alongside LLMs to generate synthetic training data or procedurally generate testing environments.
*   **Project GR00T:** NVIDIA's general-purpose foundation model for humanoid robot learning.

## 4. Recommended Pre-Reading / Watching

1.  **"Sparks of Artificial General Intelligence" (Paper/Talk by Microsoft Research):** Offers profound intuition on what LLMs are fundamentally capable of beyond text generation.
2.  **Introduction to LLM Agents (Blog posts by Lilian Weng):** Search for this incredible write-up. It breaks down Planning, Memory, and Tool Use for LLMs.
3.  **NVIDIA Isaac ROS Documentation (NVIDIA Developer site):** Quickly skim the architecture of NITROS to understand why GPU-centric ROS nodes are powerful.
4.  **"VILA: On Pre-training for Visual Language Models" (NVIDIA paper):** Skim the abstract to understand exactly how NVIDIA approaches putting vision into language models for the edge.
