import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import cv2
import numpy as np
import os

from styles import apply_custom_styles
from model_utils import (
    load_best_model,
    draw_custom_boxes,
    calculate_severity_score,
    CLASS_NAMES,
    CLASS_COLORS_HEX
)

# Page configuration
st.set_page_config(
    page_title="RoadGuard Pro | YOLOv8 Road Damage Detection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply sleek dark-mode glassmorphism styles
apply_custom_styles()

# Header Section
st.markdown('<div class="main-header">🛡️ RoadGuard Pro: Autonomous Road Damage Detection</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">High-Precision Infrastructure Inspection powered by best-performing YOLOv8 Architecture</div>', unsafe_allow_html=True)

# Load best model and display quick sidebar status
with st.sidebar:
    st.markdown("### ⚙️ Engine Status")
    try:
        model, model_path = load_best_model()
        st.success("✅ Best Model Loaded (`YOLOv8m` / `best_overall_model`)")
        st.caption("Source: `Hugging Face Hub` (`mostafaasaad32/yolo_road_crack_detection`)")
    except Exception as e:
        st.error(f"❌ Error loading model: {e}")
        st.stop()
        
    st.markdown("---")
    st.markdown("### 🎯 Detection Settings")
    conf_thresh = st.slider("Confidence Threshold", min_value=0.10, max_value=0.90, value=0.25, step=0.05, help="Minimum confidence required to display a detection bounding box.")
    iou_thresh = st.slider("IoU Threshold (NMS)", min_value=0.10, max_value=0.90, value=0.45, step=0.05, help="Intersection over Union threshold for Non-Maximum Suppression.")
    
    st.markdown("---")
    st.markdown("### 🏷️ Damage Classes")
    for cls_id, cls_name in CLASS_NAMES.items():
        color = CLASS_COLORS_HEX.get(cls_id, "#FFF")
        st.markdown(f'<span class="pill-badge" style="background: {color}22; color: {color}; border: 1px solid {color}55;">{cls_name}</span>', unsafe_allow_html=True)

# Create Navigation Tabs
tab1, tab2 = st.tabs([
    "📊 Dashboard & Comparative Analysis", 
    "🖼️ Image & Batch Detection"
])

# ==============================================================================
# TAB 1: Dashboard & Comparative Analysis
# ==============================================================================
with tab1:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 🏆 Comparative Evaluation Summary")
    st.markdown("""
    During our comprehensive architectural exploration, three distinct variants of **YOLOv8** (`YOLOv8n`, `YOLOv8s`, and `YOLOv8m`) were trained and evaluated across the **RDD2022 dataset** for 5 critical road damage types (`longitudinal crack`, `transverse crack`, `alligator crack`, `other corruption`, and `pothole`).
    
    Based on our evaluation results, **YOLOv8m (Medium)** emerged as the undisputed leader in accuracy while preserving better-than-real-time processing speeds (>30 FPS). Therefore, **this application is dedicated purely to the best-performing model (`best_overall_model` / `YOLOv8m`)**.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # Top KPI Metrics for Best Model
    col_kpi1, col_kpi2, col_kpi3, col_kpi4 = st.columns(4)
    with col_kpi1:
        st.metric("Best Model mAP50", "57.74%", "+6.48% vs Nano")
    with col_kpi2:
        st.metric("Best Model Precision", "62.59%", "+4.90% vs Nano")
    with col_kpi3:
        st.metric("Best Model Recall", "54.56%", "+6.10% vs Nano")
    with col_kpi4:
        st.metric("Inference Speed", "33.24 FPS", "30.08 ms / frame")

    st.markdown("### 📈 Detailed Architectural Comparison")
    
    # Load or construct comparison dataframe based on Final_Models_Comparison.csv
    comp_data = {
        "Model": ["YOLOv8n (Nano)", "YOLOv8s (Small)", "YOLOv8m (Medium) - [SELECTED BEST]"],
        "mAP50": [0.5126, 0.5604, 0.5774],
        "mAP50-95": [0.2587, 0.2898, 0.3018],
        "Precision": [0.5769, 0.5988, 0.6259],
        "Recall": [0.4846, 0.5426, 0.5456],
        "Size_MB": [5.96, 21.47, 49.62],
        "Inference_ms": [14.10, 20.03, 30.08],
        "FPS": [70.91, 49.92, 33.24]
    }
    df_comp = pd.DataFrame(comp_data)
    
    # Display comparison dataframe cleanly
    st.dataframe(
        df_comp.style.format({
            "mAP50": "{:.4f}",
            "mAP50-95": "{:.4f}",
            "Precision": "{:.4f}",
            "Recall": "{:.4f}",
            "Size_MB": "{:.2f} MB",
            "Inference_ms": "{:.2f} ms",
            "FPS": "{:.2f}"
        }),
        use_container_width=True
    )

    # Plotly Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        fig_map = px.bar(
            df_comp, 
            x="Model", 
            y=["mAP50", "Precision", "Recall"],
            barmode="group",
            title="Accuracy Metrics Comparison across YOLOv8 Variants",
            labels={"value": "Score", "variable": "Metric"},
            color_discrete_sequence=["#06B6D4", "#6366F1", "#10B981"]
        )
        fig_map.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font=dict(color="#F8FAFC", family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_chart2:
        fig_scatter = px.scatter(
            df_comp,
            x="FPS",
            y="mAP50",
            size="Size_MB",
            color="Model",
            title="Accuracy (mAP50) vs. Speed (FPS) Trade-off (Bubble Size = Model Size MB)",
            color_discrete_sequence=["#06B6D4", "#F97316", "#6366F1"]
        )
        # Add real-time threshold line
        fig_scatter.add_vline(x=30.0, line_dash="dash", line_color="#EF4444", annotation_text="30 FPS Real-Time Benchmark")
        fig_scatter.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.6)",
            font=dict(color="#F8FAFC", family="Inter"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # In-depth Discussion Card
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown("### 💡 Comprehensive Discussion of Results")
    st.markdown("""
    #### 1. Why `YOLOv8m` is the Best Choice for Road Damage
    Detecting road surface anomalies differs fundamentally from standard general object detection. Hairline cracks (`longitudinal` and `transverse`) and complex pavement failures (`alligator cracks`) exhibit low visual contrast and irregular morphologies that blend into surrounding asphalt texture.
    
    - **Feature Representation**: `YOLOv8m` (~25.9M parameters) possesses significantly deeper convolutional layers and higher capacity in the `C2f` modules compared to `YOLOv8n` (~3.0M parameters). This allows it to capture multi-scale spatial dependencies and subtle texture differentials required to separate actual structural degradation from shadows, water stains, and pavement joints.
    - **Significant Accuracy Margin**: `YOLOv8m` delivers a substantial **+6.48% jump in mAP50** (57.74% vs 51.26%) and **+4.31% in strict mAP50-95** (30.18% vs 25.87%) over `YOLOv8n`. Moreover, its **Precision reaches 62.59%**, drastically reducing false alarms which is vital for municipal road maintenance planning.

    #### 2. Speed vs. Accuracy Evaluation & Real-Time Feasibility
    - **Ultra-Fast Nano (`YOLOv8n`)**: Running at **70.91 FPS (14.1 ms)**, Nano is ideal for extreme resource-constrained micro-edge hardware (e.g. low-power IoT microcontrollers or inexpensive mobile phones mounted on fleet vehicle windshields). However, its lower recall (48.46%) means it misses ~51% of subtle cracks.
    - **Balanced Small (`YOLOv8s`)**: Offers a solid middle ground (**56.04% mAP50 at 49.92 FPS**).
    - **Real-Time Medium (`YOLOv8m`)**: Despite being ~8x larger in disk size than Nano (49.62 MB vs 5.96 MB), `YOLOv8m` achieves an impressive **33.24 FPS (30.08 ms inference latency)** on modern GPU execution environments. Since video feeds generally run at **25 to 30 FPS**, `YOLOv8m` comfortably exceeds the real-time threshold without sacrificing high-precision detection.
    
    #### 3. Final Deployment Decision
    By dedicating this production application exclusively to **`YOLOv8m` (`best_overall_model`)**, we guarantee that road engineers and autonomous inspection vehicles achieve the highest possible detection fidelity and automated severity assessment while maintaining smooth, responsive real-time inference.
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================================================
# TAB 2: Image & Batch Detection
# ==============================================================================
with tab2:
    st.markdown("### 🖼️ Upload & Analyze Road Surface Imagery")
    st.caption("Upload one or more road inspection images (`jpg`, `jpeg`, `png`, `webp`) for instant AI analysis using `YOLOv8m`.")
    
    uploaded_images = st.file_uploader(
        "Select Road Images", 
        type=["jpg", "jpeg", "png", "webp"], 
        accept_multiple_files=True,
        help="Upload multiple images for batch analysis and summary reporting."
    )
    
    if uploaded_images:
        batch_summary_rows = []
        
        for idx, img_file in enumerate(uploaded_images):
            image_pil = Image.open(img_file).convert("RGB")
            
            # Run YOLO inference
            results = model.predict(image_pil, conf=conf_thresh, iou=iou_thresh, verbose=False)
            
            # Draw custom boxes & extract summary
            annotated_pil, detections_list = draw_custom_boxes(image_pil, results, conf_threshold=conf_thresh)
            
            # Calculate severity score
            sev_score, sev_label, sev_color = calculate_severity_score(detections_list)
            
            st.markdown(f'<div class="premium-card">', unsafe_allow_html=True)
            st.markdown(f"#### 🔍 Image #{idx+1}: `{img_file.name}`")
            
            col_img, col_metrics = st.columns([1.3, 1])
            with col_img:
                st.image(annotated_pil, caption=f"Annotated Output ({len(detections_list)} damages detected)", use_column_width=True)
                
            with col_metrics:
                st.markdown(f"**Road Severity Assessment:**")
                st.markdown(f'<span class="pill-badge" style="background: {sev_color}22; color: {sev_color}; border: 1px solid {sev_color}66; font-size: 0.95rem; padding: 0.5rem 1rem;">{sev_label} (Index: {sev_score}/100)</span>', unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                col_sub1, col_sub2 = st.columns(2)
                with col_sub1:
                    st.metric("Detected Damages", len(detections_list))
                with col_sub2:
                    avg_conf = np.mean([d["Confidence"] for d in detections_list]) if detections_list else 0.0
                    st.metric("Avg Confidence", f"{avg_conf:.1f}%")
                    
                # Breakdown by category
                if detections_list:
                    st.markdown("**Damage Breakdown:**")
                    df_det = pd.DataFrame(detections_list)
                    counts = df_det["Damage Type"].value_counts().reset_index()
                    counts.columns = ["Damage Type", "Count"]
                    st.table(counts)
                    
                    # Prepare rows for overall batch export
                    for d in detections_list:
                        batch_summary_rows.append({
                            "Image File": img_file.name,
                            "Damage Type": d["Damage Type"],
                            "Confidence (%)": d["Confidence"],
                            "Bounding Box": d["Bounding Box"],
                            "Severity Index": sev_score,
                            "Assessment": sev_label
                        })
                else:
                    st.info("✨ No road surface defects detected above the confidence threshold.")
                    batch_summary_rows.append({
                        "Image File": img_file.name,
                        "Damage Type": "None",
                        "Confidence (%)": 0.0,
                        "Bounding Box": "[]",
                        "Severity Index": 0.0,
                        "Assessment": "Excellent (No Visible Damage)"
                    })
                    
            st.markdown('</div>', unsafe_allow_html=True)
            
        # Batch CSV Export Button
        if batch_summary_rows:
            df_export = pd.DataFrame(batch_summary_rows)
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Batch Detection Report (CSV)",
                data=csv_data,
                file_name="road_damage_batch_report.csv",
                mime="text/csv",
                type="primary",
                use_container_width=True
            )
    else:
        st.info("👋 Please upload one or more road inspection images above to begin real-time detection.")


