import openai
import streamlit as st
import json
import requests
from typing import Dict, List, Any
import time

class DesignAnalysisAgent:
    def __init__(self, api_key: str):
        """Initialize the design analysis agent with GPT API"""
        self.client = openai.OpenAI(api_key=api_key)
        self.system_prompt = """
        You are an expert UX/UI design consultant and creative strategist with deep knowledge of:
        - Modern web design trends and best practices
        - User experience psychology and behavior patterns
        - Visual hierarchy and information architecture
        - Brand identity and design systems
        - Conversion optimization and user engagement
        - Accessibility and inclusive design
        - Mobile-first and responsive design principles
        
        Your role is to analyze design concepts and provide actionable improvements that enhance:
        1. User engagement and conversion rates
        2. Visual appeal and brand consistency
        3. Usability and accessibility
        4. Modern design trends and innovation
        5. Technical feasibility and performance
        
        Always provide specific, actionable recommendations with clear reasoning.
        """
    
    def analyze_design_concept(self, design_description: str, target_audience: str = "general users") -> Dict[str, Any]:
        """Analyze a design concept and provide improvement recommendations"""
        
        prompt = f"""
        Analyze this design concept and provide comprehensive improvement recommendations:
        
        DESIGN CONCEPT:
        {design_description}
        
        TARGET AUDIENCE: {target_audience}
        
        Please provide analysis in the following JSON format:
        {{
            "overall_score": 85,
            "strengths": ["list of design strengths"],
            "weaknesses": ["list of areas for improvement"],
            "recommendations": {{
                "visual_design": ["specific visual improvements"],
                "user_experience": ["UX enhancement suggestions"],
                "functionality": ["feature and interaction improvements"],
                "accessibility": ["accessibility enhancements"],
                "modern_trends": ["trendy design elements to incorporate"]
            }},
            "inspiration_sources": ["relevant design inspiration"],
            "implementation_priority": ["ordered list of improvements by priority"],
            "estimated_impact": "description of expected improvements"
        }}
        
        Focus on practical, implementable suggestions that will significantly improve the design.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            analysis = json.loads(response.choices[0].message.content)
            return analysis
            
        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}
    
    def generate_design_variations(self, original_concept: str, style_preference: str = "modern") -> List[Dict[str, str]]:
        """Generate multiple design variations based on the original concept"""
        
        prompt = f"""
        Based on this design concept, generate 3 different design variations:
        
        ORIGINAL CONCEPT:
        {original_concept}
        
        STYLE PREFERENCE: {style_preference}
        
        Generate variations in this JSON format:
        {{
            "variations": [
                {{
                    "name": "Variation 1 Name",
                    "description": "Detailed description of the variation",
                    "key_features": ["feature1", "feature2", "feature3"],
                    "color_scheme": "description of color palette",
                    "layout_approach": "description of layout strategy",
                    "unique_elements": ["element1", "element2"],
                    "target_use_case": "when to use this variation"
                }}
            ]
        }}
        
        Make each variation distinctly different while maintaining the core concept.
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            variations = json.loads(response.choices[0].message.content)
            return variations.get("variations", [])
            
        except Exception as e:
            return [{"error": f"Variation generation failed: {str(e)}"}]
    
    def create_implementation_guide(self, design_concept: str, improvements: List[str]) -> Dict[str, Any]:
        """Create a step-by-step implementation guide for design improvements"""
        
        prompt = f"""
        Create a detailed implementation guide for these design improvements:
        
        DESIGN CONCEPT:
        {design_concept}
        
        IMPROVEMENTS TO IMPLEMENT:
        {', '.join(improvements)}
        
        Provide implementation guide in this JSON format:
        {{
            "phases": [
                {{
                    "phase": "Phase 1: Foundation",
                    "duration": "1-2 weeks",
                    "tasks": ["task1", "task2", "task3"],
                    "deliverables": ["deliverable1", "deliverable2"],
                    "resources_needed": ["resource1", "resource2"],
                    "success_metrics": ["metric1", "metric2"]
                }}
            ],
            "tools_recommended": ["tool1", "tool2", "tool3"],
            "timeline": "overall timeline description",
            "budget_estimate": "cost estimate",
            "risk_factors": ["risk1", "risk2"],
            "success_criteria": ["criteria1", "criteria2"]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2000
            )
            
            guide = json.loads(response.choices[0].message.content)
            return guide
            
        except Exception as e:
            return {"error": f"Guide creation failed: {str(e)}"}

def main():
    st.set_page_config(
        page_title="Design Analysis Agent",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 AI Design Analysis Agent")
    st.markdown("### Get expert design recommendations and improvements for your concepts")
    
    # API Key input
    api_key = st.sidebar.text_input("Enter your OpenAI API Key:", type="password")
    
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to use the design agent.")
        st.info("""
        **How to get an API key:**
        1. Go to [OpenAI Platform](https://platform.openai.com/)
        2. Sign up or log in
        3. Navigate to API Keys section
        4. Create a new API key
        5. Copy and paste it here
        """)
        return
    
    # Initialize agent
    agent = DesignAnalysisAgent(api_key)
    
    # Main interface
    tab1, tab2, tab3 = st.tabs(["📊 Design Analysis", "🎨 Design Variations", "📋 Implementation Guide"])
    
    with tab1:
        st.header("Design Concept Analysis")
        
        design_concept = st.text_area(
            "Describe your design concept:",
            placeholder="Describe your design concept, layout, color scheme, target audience, and goals...",
            height=150
        )
        
        target_audience = st.selectbox(
            "Target Audience:",
            ["General Users", "Business Professionals", "Young Adults (18-25)", "Seniors (65+)", "Children", "Tech Enthusiasts", "Creative Professionals"]
        )
        
        if st.button("🔍 Analyze Design", type="primary"):
            if design_concept.strip():
                with st.spinner("Analyzing your design concept..."):
                    analysis = agent.analyze_design_concept(design_concept, target_audience)
                    
                    if "error" not in analysis:
                        # Display analysis results
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Overall Score", f"{analysis['overall_score']}/100")
                            
                            st.subheader("✅ Strengths")
                            for strength in analysis['strengths']:
                                st.write(f"• {strength}")
                        
                        with col2:
                            st.subheader("⚠️ Areas for Improvement")
                            for weakness in analysis['weaknesses']:
                                st.write(f"• {weakness}")
                        
                        # Detailed recommendations
                        st.subheader("🎯 Detailed Recommendations")
                        
                        recommendations = analysis['recommendations']
                        cols = st.columns(2)
                        
                        with cols[0]:
                            st.markdown("**🎨 Visual Design**")
                            for rec in recommendations['visual_design']:
                                st.write(f"• {rec}")
                            
                            st.markdown("**👥 User Experience**")
                            for rec in recommendations['user_experience']:
                                st.write(f"• {rec}")
                        
                        with cols[1]:
                            st.markdown("**⚙️ Functionality**")
                            for rec in recommendations['functionality']:
                                st.write(f"• {rec}")
                            
                            st.markdown("**♿ Accessibility**")
                            for rec in recommendations['accessibility']:
                                st.write(f"• {rec}")
                        
                        # Modern trends
                        st.subheader("🚀 Modern Design Trends")
                        for trend in recommendations['modern_trends']:
                            st.write(f"• {trend}")
                        
                        # Implementation priority
                        st.subheader("📋 Implementation Priority")
                        for i, priority in enumerate(analysis['implementation_priority'], 1):
                            st.write(f"{i}. {priority}")
                        
                        # Expected impact
                        st.subheader("📈 Expected Impact")
                        st.info(analysis['estimated_impact'])
                        
                    else:
                        st.error(f"Analysis failed: {analysis['error']}")
            else:
                st.warning("Please describe your design concept.")
    
    with tab2:
        st.header("Design Variations Generator")
        
        original_concept = st.text_area(
            "Original Design Concept:",
            placeholder="Describe your original design concept...",
            height=100
        )
        
        style_preference = st.selectbox(
            "Style Preference:",
            ["Modern", "Minimalist", "Bold & Colorful", "Professional", "Playful", "Luxury", "Tech-focused", "Eco-friendly"]
        )
        
        if st.button("🎨 Generate Variations", type="primary"):
            if original_concept.strip():
                with st.spinner("Generating design variations..."):
                    variations = agent.generate_design_variations(original_concept, style_preference)
                    
                    if variations and "error" not in variations[0]:
                        for i, variation in enumerate(variations, 1):
                            with st.expander(f"🎨 Variation {i}: {variation['name']}"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown(f"**Description:** {variation['description']}")
                                    st.markdown(f"**Color Scheme:** {variation['color_scheme']}")
                                    st.markdown(f"**Layout Approach:** {variation['layout_approach']}")
                                
                                with col2:
                                    st.markdown("**Key Features:**")
                                    for feature in variation['key_features']:
                                        st.write(f"• {feature}")
                                    
                                    st.markdown("**Unique Elements:**")
                                    for element in variation['unique_elements']:
                                        st.write(f"• {element}")
                                
                                st.markdown(f"**Best for:** {variation['target_use_case']}")
                    else:
                        st.error("Failed to generate variations.")
            else:
                st.warning("Please describe your original design concept.")
    
    with tab3:
        st.header("Implementation Guide Generator")
        
        concept_for_guide = st.text_area(
            "Design Concept for Implementation:",
            placeholder="Describe the design concept you want to implement...",
            height=100
        )
        
        improvements_input = st.text_area(
            "Improvements to Implement (one per line):",
            placeholder="Enter each improvement on a new line...",
            height=100
        )
        
        if st.button("📋 Generate Implementation Guide", type="primary"):
            if concept_for_guide.strip() and improvements_input.strip():
                improvements = [imp.strip() for imp in improvements_input.split('\n') if imp.strip()]
                
                with st.spinner("Creating implementation guide..."):
                    guide = agent.create_implementation_guide(concept_for_guide, improvements)
                    
                    if "error" not in guide:
                        # Display implementation phases
                        st.subheader("📅 Implementation Phases")
                        
                        for phase in guide['phases']:
                            with st.expander(f"📋 {phase['phase']} ({phase['duration']})"):
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    st.markdown("**Tasks:**")
                                    for task in phase['tasks']:
                                        st.write(f"• {task}")
                                    
                                    st.markdown("**Deliverables:**")
                                    for deliverable in phase['deliverables']:
                                        st.write(f"• {deliverable}")
                                
                                with col2:
                                    st.markdown("**Resources Needed:**")
                                    for resource in phase['resources_needed']:
                                        st.write(f"• {resource}")
                                    
                                    st.markdown("**Success Metrics:**")
                                    for metric in phase['success_metrics']:
                                        st.write(f"• {metric}")
                        
                        # Additional information
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🛠️ Recommended Tools")
                            for tool in guide['tools_recommended']:
                                st.write(f"• {tool}")
                            
                            st.subheader("💰 Budget Estimate")
                            st.info(guide['budget_estimate'])
                        
                        with col2:
                            st.subheader("⚠️ Risk Factors")
                            for risk in guide['risk_factors']:
                                st.write(f"• {risk}")
                            
                            st.subheader("✅ Success Criteria")
                            for criteria in guide['success_criteria']:
                                st.write(f"• {criteria}")
                        
                        st.subheader("📈 Timeline")
                        st.info(guide['timeline'])
                        
                    else:
                        st.error(f"Guide creation failed: {guide['error']}")
            else:
                st.warning("Please provide both design concept and improvements.")

if __name__ == "__main__":
    main()
