"""
SalaryPredictorApp.py

A Streamlit-based web application for predicting salaries based on years of experience.

This script serves as the entry point for the app. It initializes and runs the 
SalaryPredictorApp class, which loads a trained model and provides a user-friendly 
interface for input and prediction.

Author: Nhan Pham
Email: ptnhanit230104@gmail.com
Date: 2025-07-26
Version: 1.0.1 (Corrected path handling)
"""

import streamlit as st
import pickle
from pathlib import Path # Import Path for robust path handling

class SalaryPredictorApp:
    """
    A Streamlit-based web application to predict salary based on years of experience.
    """

    def __init__(self):
        """Initializes the SalaryPredictorApp by loading the model and setting up the page."""
        self.model = self.load_model()
        self.setup_page()

    def load_model(self):
        """
        Loads a trained machine learning model from a pickle file using a path 
        relative to the current script's location.

        Returns:
            sklearn.base.BaseEstimator or None: The trained model, or None if loading failed.
        """
        try:
            # 1. Get the directory of the current script (SalaryPredictorApp.py)
            script_dir = Path(__file__).parent
            
            # 2. Construct the absolute path based on the relative structure: 
            #    script_dir / .. / model / model.pkl
            model_path = script_dir.parent / 'model' / 'model.pkl'

            with open(model_path, 'rb') as file:
                st.sidebar.success("✅ Model loaded successfully.")
                return pickle.load(file)
                
        except FileNotFoundError:
            st.error(f"**Error: Model file not found.**")
            st.warning(f"Expected to find 'model.pkl' at: `{model_path.resolve()}`")
            st.info("Please ensure your file structure is correct: `app/` and `model/model.pkl` should be siblings.")
            return None
        except Exception as e:
            st.error(f"An unexpected error occurred while loading the model: {e}")
            return None

    def setup_page(self):
        """
        Configures the Streamlit page with a title, icon, and layout.
        """
        
        # Beautiful full-bleed background with a glass card for content
        st.markdown(
            """
            <style>
            /* Full page gradient background */
            .app-bg {
                position: fixed;
                inset: 0;
                background: radial-gradient(ellipse at 10% 10%, rgba(76,175,80,0.10) 0%, rgba(76,175,80,0.02) 25%),
                            linear-gradient(135deg, #0f172a 0%, #0b2545 50%, #04263a 100%);
                z-index: -1;
                overflow: hidden;
            }

            /* Subtle animated circles */
            .bg-circle {
                position: absolute;
                border-radius: 50%;
                filter: blur(80px);
                opacity: 0.35;
                animation: float 12s ease-in-out infinite;
            }

            .bg-circle.c1 { width: 420px; height: 420px; left: -80px; top: -40px; background: #1abc9c; }
            .bg-circle.c2 { width: 360px; height: 360px; right: -120px; top: 60px; background: #4caf50; animation-duration: 18s; }
            .bg-circle.c3 { width: 500px; height: 500px; left: 30%; bottom: -200px; background: #3b82f6; animation-duration: 20s; }

            @keyframes float {
                0% { transform: translateY(0) translateX(0); }
                50% { transform: translateY(-30px) translateX(20px); }
                100% { transform: translateY(0) translateX(0); }
            }

            /* Glass card where the app widgets sit */
            .glass-card {
                background: rgba(255, 255, 255, 0.06);
                backdrop-filter: blur(8px) saturate(120%);
                -webkit-backdrop-filter: blur(8px) saturate(120%);
                border: 1px solid rgba(255,255,255,0.06);
                border-radius: 12px;
                padding: 24px;
                box-shadow: 0 8px 30px rgba(2,6,23,0.6);
            }

            /* Title styling inside Streamlit markdown */
            .app-title { text-align: center; color: #e6fff2; font-size: 28px; font-weight: 700; margin-bottom: 6px; }
            .app-sub { text-align: center; color: #cdeed9; margin-top: 0; margin-bottom: 18px; }

            /* Make Streamlit button rounded and full width */
            .stButton>button {
                border-radius: 8px;
                padding: 10px 14px;
            }
            
            /* Apply glass-card style to the main Streamlit container */
            .css-usj99p {
                margin-top: 5rem; /* Push content down to compensate for fixed background */
            }

            </style>

            <div class="app-bg" aria-hidden="true">
                <div class="bg-circle c1"></div>
                <div class="bg-circle c2"></div>
                <div class="bg-circle c3"></div>
            </div>
            
            <div class="glass-card">
                <div class="app-title">Salary Prediction App</div>
                <div class="app-sub">Predict the salary based on years of experience.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Add a little spacing so the rest of the Streamlit UI appears inside the glass card visually
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    def get_user_input(self):
        """
        Renders a number input widget to get years of experience from the user.

        Returns:
            int: The number of years of experience entered by the user.
        """
        return st.number_input(
            "Enter years of experience:",
            min_value=0.0,
            max_value=50.0,
            value=1.0, # Start with a non-zero value
            step=0.5,
            format="%.1f"
        )

    def predict_salary(self, experience):
        """
        Predicts salary based on the number of years of experience.

        Args:
            experience (float): Years of experience.

        Returns:
            float: The predicted salary.
        """
        # Note: The model expects a 2D array, so we wrap the input in [[...]]
        return self.model.predict([[experience]])[0]

    def run(self):
        """
        Runs the main app logic:
            - Gets user input
            - Predicts salary if the model loaded and the button is clicked
            - Displays the result
        """
        if self.model is None:
            # Do not proceed if the model failed to load
            st.stop()
            
        experience = self.get_user_input()
        
        # Ensure experience is a float for prediction
        experience_float = float(experience) 

        if st.button(label="💰 Predict Salary", use_container_width=True):
            # Predict only if the model is loaded successfully
            if self.model:
                salary = self.predict_salary(experience_float)
                
                # Enhanced result display
                st.markdown("---")
                st.balloons()
                st.success(
                    f"### Predicted Salary for {experience_float} Years Experience"
                )
                
                # Use a metric for a cleaner look
                st.metric(
                    label="Estimated Annual Salary",
                    value=f"${salary:,.2f}"
                )
