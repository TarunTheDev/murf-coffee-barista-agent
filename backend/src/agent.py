import logging
import json
from pathlib import Path
from typing import Optional
import datetime
import asyncio

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class CoffeeOrder:
    """Represents a coffee order with all its details."""
    def __init__(self):
        self.drink_type: Optional[str] = None
        self.size: Optional[str] = None
        self.milk: Optional[str] = None
        self.extras: list[str] = []
        self.name: Optional[str] = None
    
    def is_complete(self) -> bool:
        """Check if all required fields are filled."""
        return all([
            self.drink_type,
            self.size,
            self.milk,
            self.name
        ])
    
    def to_dict(self) -> dict:
        """Convert order to dictionary format."""
        return {
            "drinkType": self.drink_type,
            "size": self.size,
            "milk": self.milk,
            "extras": self.extras,
            "name": self.name
        }
    
    def generate_beverage_html(self) -> str:
        """Generate HTML visualization of the beverage."""
        # Cup sizes - more realistic proportions
        cup_heights = {"small": "180px", "medium": "220px", "large": "260px"}
        cup_widths = {"small": "110px", "medium": "130px", "large": "150px"}
        
        height = cup_heights.get(self.size or "medium", "220px")
        width = cup_widths.get(self.size or "medium", "130px")
        
        # Check for whipped cream in extras
        has_whipped_cream = any("whipped" in extra or "cream" in extra for extra in self.extras)
        
        # Drink colors - more realistic coffee colors
        drink_colors = {
            "latte": "#c49a6c",
            "cappuccino": "#b88a5e", 
            "espresso": "#3e2723",
            "americano": "#5d4037",
            "mocha": "#6d4c41",
            "flat white": "#d4a574",
        }
        
        drink_color = drink_colors.get(self.drink_type or "latte", "#c49a6c")
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @keyframes slideIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .coffee-container {{
                    animation: slideIn 0.6s ease-out;
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 0;">
        <div class="coffee-container" style="display: flex; flex-direction: column; align-items: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">
            <h2 style="color: white; margin-bottom: 25px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); font-size: 28px; letter-spacing: 1px;">☕ Your Perfect Coffee</h2>
            
            <!-- Beverage Visualization -->
            <div style="position: relative; margin-bottom: 35px; transform-style: preserve-3d;">
                
                <!-- Coffee Cup - Modern Minimalist Style -->
                <div style="position: relative; width: {width}; height: {height}; 
                    background: linear-gradient(165deg, {drink_color} 0%, {drink_color}dd 100%);
                    border-radius: 8px 8px 35px 35px; 
                    box-shadow: 
                        0 25px 50px rgba(0,0,0,0.35),
                        inset -8px 0 15px rgba(0,0,0,0.2),
                        inset 8px 0 15px rgba(255,255,255,0.1);
                    border: 3px solid rgba(139,111,71,0.8);
                    overflow: visible;">
                    
                    <!-- Foam/Milk Layer - Realistic -->
                    <div style="position: absolute; top: 0; left: 0; right: 0; height: 22%; 
                        background: linear-gradient(180deg, 
                            rgba(255,248,240,0.95) 0%, 
                            rgba(245,235,220,0.85) 40%,
                            rgba(240,230,215,0.6) 70%,
                            transparent 100%);
                        border-radius: 8px 8px 50% 50% / 8px 8px 35% 35%;
                        box-shadow: inset 0 -3px 8px rgba(0,0,0,0.08);"></div>
                    
                    <!-- Coffee Shine/Highlight -->
                    <div style="position: absolute; top: 20%; left: 12%; width: 25%; height: 35%; 
                        background: linear-gradient(135deg, rgba(255,255,255,0.25) 0%, transparent 60%); 
                        border-radius: 40% 60% 50% 70%;
                        filter: blur(8px);"></div>
                    
                    <!-- Whipped Cream - Simple and Clean -->
                    {f'''<div style="position: absolute; top: -22px; left: 50%; transform: translateX(-50%); 
                        width: calc({cup_widths.get(self.size or 'medium', '130px')} - 10px); 
                        height: 35px; 
                        background: linear-gradient(180deg, #ffffff 0%, #fffbf5 50%, #f5f0e8 100%); 
                        border-radius: 50%; 
                        box-shadow: 
                            0 -2px 8px rgba(255,255,255,0.8),
                            0 4px 12px rgba(0,0,0,0.2),
                            inset 0 -2px 5px rgba(0,0,0,0.05);
                        z-index: 5;
                    "></div>''' if has_whipped_cream else ''}
                    
                    <!-- Cup Handle - Clean Design -->
                    <div style="position: absolute; right: -38px; top: 30%; 
                        width: 45px; height: 42%; 
                        border: 4px solid rgba(139,111,71,0.9); 
                        border-left: none; 
                        border-radius: 0 45% 45% 0;
                        box-shadow: 
                            inset -2px 0 6px rgba(0,0,0,0.25),
                            2px 3px 10px rgba(0,0,0,0.3);"></div>
                </div>
                
                <!-- Saucer - Simple and Elegant -->
                <div style="width: calc({width} + 50px); height: 16px; 
                    background: linear-gradient(180deg, #9d826d 0%, #8b6f47 100%); 
                    border-radius: 50%; 
                    margin-top: 6px;
                    box-shadow: 
                        0 8px 20px rgba(0,0,0,0.35),
                        inset 0 2px 6px rgba(255,255,255,0.15);
                    border: 2px solid #6d5638;"></div>
            </div>
            
            <!-- Order Details -->
            <div style="background: white; padding: 25px; border-radius: 18px; width: 100%; max-width: 450px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); animation: slideIn 0.8s ease-out 0.2s both;">
                <h3 style="margin-top: 0; color: #4a2c2a; border-bottom: 3px solid #667eea; padding-bottom: 12px; font-size: 24px; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 28px;">📋</span> Order Summary
                </h3>
                
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%); border-radius: 10px; border-left: 4px solid #667eea;">
                        <strong style="color: #555; font-size: 16px;">👤 Customer:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{self.name or "N/A"}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fff8f0 0%, #fff0e6 100%); border-radius: 10px; border-left: 4px solid #d4a574;">
                        <strong style="color: #555; font-size: 16px;">☕ Drink:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.drink_type or "N/A").title()}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f0fff4 0%, #e6f9f0 100%); border-radius: 10px; border-left: 4px solid #52c41a;">
                        <strong style="color: #555; font-size: 16px;">📏 Size:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.size or "N/A").title()}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fffbf0 0%, #fff5e6 100%); border-radius: 10px; border-left: 4px solid #faad14;">
                        <strong style="color: #555; font-size: 16px;">🥛 Milk:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.milk or "N/A").title()}</span>
                    </div>
                    
                    {f'''<div style="margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fff0f6 0%, #ffe6f0 100%); border-radius: 10px; border-left: 4px solid #eb2f96;">
                        <strong style="color: #555; font-size: 16px; display: block; margin-bottom: 8px;">✨ Extras:</strong>
                        <ul style="margin: 5px 0; padding-left: 25px; color: #222;">
                            {"".join(f"<li style='margin: 5px 0; font-weight: 500;'>{extra.title()}</li>" for extra in self.extras)}
                        </ul>
                    </div>''' if self.extras else '<div style="margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f5f5f5 0%, #ebebeb 100%); border-radius: 10px; border-left: 4px solid #d9d9d9;"><strong style="color: #555; font-size: 16px;">✨ Extras:</strong> <span style="color: #999; font-style: italic;">None</span></div>'}
                </div>
                
                <div style="margin-top: 25px; padding-top: 20px; border-top: 2px dashed #ddd; text-align: center;">
                    <p style="color: #667eea; font-weight: bold; font-size: 22px; margin: 8px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                        Order #{datetime.datetime.now().strftime("%Y%m%d%H%M%S")[-6:]}
                    </p>
                    <p style="color: #999; font-size: 14px; margin: 5px 0; font-weight: 500;">
                        {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                    </p>
                </div>
            </div>
            
            <p style="color: white; margin-top: 25px; font-size: 16px; text-align: center; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); font-weight: 500;">
                ✨ Thank you for ordering from Murf Coffee Shop! ✨
            </p>
        </div>
        </body>
        </html>
        """
        
        return html
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                @keyframes float {{
                    0%, 100% {{ transform: translateY(0px); }}
                    50% {{ transform: translateY(-10px); }}
                }}
                @keyframes steam {{
                    0% {{ opacity: 0.7; transform: translateY(0) scale(1); }}
                    100% {{ opacity: 0; transform: translateY(-40px) scale(1.5); }}
                }}
                @keyframes pulse {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.02); }}
                }}
                @keyframes slideIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                .coffee-container {{
                    animation: slideIn 0.8s ease-out;
                }}
                .cup-wrapper {{
                    animation: float 3s ease-in-out infinite;
                }}
            </style>
        </head>
        <body style="margin: 0; padding: 0;">
        <div class="coffee-container" style="display: flex; flex-direction: column; align-items: center; padding: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 20px; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; min-height: 500px;">
            <h2 style="color: white; margin-bottom: 30px; text-shadow: 2px 2px 8px rgba(0,0,0,0.4); font-size: 28px; letter-spacing: 1px;">☕ Your Perfect Coffee</h2>
            
            <!-- Beverage Visualization -->
            <div class="cup-wrapper" style="position: relative; margin-bottom: 40px; filter: drop-shadow(0 20px 40px rgba(0,0,0,0.4));">
                
                <!-- Steam Animation -->
                <div style="position: absolute; top: -60px; left: 50%; transform: translateX(-50%); width: 100%; height: 60px; overflow: hidden; z-index: 15;">
                    <div style="position: absolute; left: 30%; width: 8px; height: 40px; background: linear-gradient(180deg, rgba(255,255,255,0.6) 0%, transparent 100%); border-radius: 50%; animation: steam 2s ease-in-out infinite; animation-delay: 0s;"></div>
                    <div style="position: absolute; left: 50%; width: 10px; height: 45px; background: linear-gradient(180deg, rgba(255,255,255,0.5) 0%, transparent 100%); border-radius: 50%; animation: steam 2.5s ease-in-out infinite; animation-delay: 0.5s;"></div>
                    <div style="position: absolute; left: 65%; width: 7px; height: 35px; background: linear-gradient(180deg, rgba(255,255,255,0.6) 0%, transparent 100%); border-radius: 50%; animation: steam 2.2s ease-in-out infinite; animation-delay: 1s;"></div>
                </div>
                
                <!-- Whipped Cream (if present) -->
                {f'''<div style="position: absolute; top: -35px; left: 50%; transform: translateX(-50%); 
                    width: calc({cup_widths.get(self.size or 'medium', '170px')} + 10px); height: 55px; 
                    background: radial-gradient(ellipse at center, #ffffff 0%, #fff8f0 40%, #f5f5f0 100%); 
                    border-radius: 60% 60% 50% 50% / 70% 70% 40% 40%; 
                    box-shadow: 
                        inset 0 -8px 15px rgba(0,0,0,0.08),
                        0 8px 20px rgba(0,0,0,0.15),
                        inset 0 2px 10px rgba(255,255,255,0.9);
                    z-index: 12;
                    animation: pulse 2s ease-in-out infinite;
                "></div>
                <div style="position: absolute; top: -42px; left: 52%; transform: translateX(-50%); 
                    width: calc({cup_widths.get(self.size or 'medium', '170px')} * 0.6); height: 30px; 
                    background: radial-gradient(ellipse at center, #ffffff 0%, #fefdf8 60%, #f8f6f0 100%); 
                    border-radius: 50%; 
                    box-shadow: inset 0 -3px 8px rgba(0,0,0,0.06);
                    z-index: 13;
                "></div>
                <div style="position: absolute; top: -48px; left: 48%; transform: translateX(-50%); 
                    width: calc({cup_widths.get(self.size or 'medium', '170px')} * 0.4); height: 22px; 
                    background: radial-gradient(ellipse at center, #ffffff 0%, #fffefb 70%); 
                    border-radius: 50%; 
                    box-shadow: inset 0 -2px 5px rgba(0,0,0,0.05);
                    z-index: 14;
                "></div>''' if has_whipped_cream else ''}
                
                <!-- Coffee Cup -->
                <div style="position: relative; width: {width}; height: {height}; 
                    background: {drink_color}; 
                    border-radius: 0 0 40px 40px; 
                    box-shadow: 
                        0 20px 60px rgba(0,0,0,0.4),
                        inset 0 0 50px rgba(0,0,0,0.1),
                        inset -15px 0 30px rgba(0,0,0,0.15),
                        inset 15px 0 30px rgba(255,255,255,0.1);
                    border: 4px solid #8b6f47;
                    border-top: none;
                    overflow: hidden;">
                    
                    <!-- Coffee Liquid Shine -->
                    <div style="position: absolute; top: 0; left: 15%; width: 30%; height: 60%; 
                        background: linear-gradient(135deg, rgba(255,255,255,0.3) 0%, transparent 50%); 
                        border-radius: 50%;
                        filter: blur(15px);"></div>
                    
                    <!-- Foam/Milk Layer -->
                    <div style="position: absolute; top: 0; left: 0; right: 0; height: 35%; 
                        background: 
                            radial-gradient(ellipse at 30% 20%, rgba(255,255,255,0.6) 0%, transparent 50%),
                            radial-gradient(ellipse at 70% 30%, rgba(255,255,255,0.5) 0%, transparent 50%),
                            linear-gradient(180deg, rgba(255,255,255,0.5) 0%, rgba(255,255,255,0.2) 60%, transparent 100%); 
                        border-radius: 0 0 50% 50% / 0 0 30% 30%;
                        box-shadow: inset 0 -5px 15px rgba(0,0,0,0.1);"></div>
                    
                    <!-- Foam Bubbles -->
                    <div style="position: absolute; top: 8%; left: 25%; width: 18px; height: 18px; 
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.3) 100%); 
                        border-radius: 50%; 
                        box-shadow: inset 0 2px 4px rgba(255,255,255,0.6);"></div>
                    <div style="position: absolute; top: 12%; left: 55%; width: 14px; height: 14px; 
                        background: radial-gradient(circle, rgba(255,255,255,0.7) 0%, rgba(255,255,255,0.3) 100%); 
                        border-radius: 50%;
                        box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);"></div>
                    <div style="position: absolute; top: 6%; left: 70%; width: 12px; height: 12px; 
                        background: radial-gradient(circle, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.3) 100%); 
                        border-radius: 50%;
                        box-shadow: inset 0 2px 4px rgba(255,255,255,0.6);"></div>
                    
                    <!-- Cup Handle -->
                    <div style="position: absolute; right: -45px; top: 25%; 
                        width: 55px; height: 50%; 
                        border: 6px solid #8b6f47; 
                        border-left: none; 
                        border-radius: 0 60% 60% 0;
                        background: linear-gradient(90deg, transparent 0%, rgba(139,111,71,0.1) 50%, transparent 100%);
                        box-shadow: 
                            inset -3px 0 8px rgba(0,0,0,0.3),
                            3px 5px 15px rgba(0,0,0,0.3);"></div>
                </div>
                
                <!-- Saucer -->
                <div style="width: calc({width} + 60px); height: 20px; 
                    background: linear-gradient(180deg, #a0826d 0%, #8b6f47 50%, #6d5638 100%); 
                    border-radius: 50%; 
                    margin-top: 8px;
                    box-shadow: 
                        0 10px 30px rgba(0,0,0,0.4),
                        inset 0 3px 10px rgba(255,255,255,0.2),
                        inset 0 -3px 10px rgba(0,0,0,0.3);
                    border: 3px solid #6d5638;
                    position: relative;">
                    <div style="position: absolute; top: 2px; left: 20%; width: 60%; height: 40%; 
                        background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 50%, transparent 100%); 
                        border-radius: 50%;"></div>
                </div>
            </div>
            
            <!-- Order Details -->
            <div style="background: white; padding: 25px; border-radius: 20px; width: 100%; max-width: 450px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); animation: slideIn 0.8s ease-out 0.3s both;">
                <h3 style="margin-top: 0; color: #4a2c2a; border-bottom: 3px solid #667eea; padding-bottom: 12px; font-size: 24px; display: flex; align-items: center; gap: 10px;">
                    <span style="font-size: 28px;">📋</span> Order Summary
                </h3>
                
                <div style="margin: 20px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f8f9ff 0%, #f0f2ff 100%); border-radius: 10px; border-left: 4px solid #667eea;">
                        <strong style="color: #555; font-size: 16px;">👤 Customer:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{self.name or "N/A"}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fff8f0 0%, #fff0e6 100%); border-radius: 10px; border-left: 4px solid #d4a574;">
                        <strong style="color: #555; font-size: 16px;">☕ Drink:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.drink_type or "N/A").title()}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f0fff4 0%, #e6f9f0 100%); border-radius: 10px; border-left: 4px solid #52c41a;">
                        <strong style="color: #555; font-size: 16px;">📏 Size:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.size or "N/A").title()}</span>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; align-items: center; margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fffbf0 0%, #fff5e6 100%); border-radius: 10px; border-left: 4px solid #faad14;">
                        <strong style="color: #555; font-size: 16px;">🥛 Milk:</strong>
                        <span style="color: #222; font-weight: 600; font-size: 16px;">{(self.milk or "N/A").title()}</span>
                    </div>
                    
                    {f'''<div style="margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #fff0f6 0%, #ffe6f0 100%); border-radius: 10px; border-left: 4px solid #eb2f96;">
                        <strong style="color: #555; font-size: 16px; display: block; margin-bottom: 8px;">✨ Extras:</strong>
                        <ul style="margin: 5px 0; padding-left: 25px; color: #222;">
                            {"".join(f"<li style='margin: 5px 0; font-weight: 500;'>{extra.title()}</li>" for extra in self.extras)}
                        </ul>
                    </div>''' if self.extras else '<div style="margin: 15px 0; padding: 12px; background: linear-gradient(135deg, #f5f5f5 0%, #ebebeb 100%); border-radius: 10px; border-left: 4px solid #d9d9d9;"><strong style="color: #555; font-size: 16px;">✨ Extras:</strong> <span style="color: #999; font-style: italic;">None</span></div>'}
                </div>
                
                <div style="margin-top: 25px; padding-top: 20px; border-top: 2px dashed #ddd; text-align: center;">
                    <p style="color: #667eea; font-weight: bold; font-size: 22px; margin: 8px 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.1);">
                        Order #{datetime.datetime.now().strftime("%Y%m%d%H%M%S")[-6:]}
                    </p>
                    <p style="color: #999; font-size: 14px; margin: 5px 0; font-weight: 500;">
                        {datetime.datetime.now().strftime("%B %d, %Y at %I:%M %p")}
                    </p>
                </div>
            </div>
            
            <p style="color: white; margin-top: 25px; font-size: 16px; text-align: center; text-shadow: 1px 1px 3px rgba(0,0,0,0.3); font-weight: 500;">
                ✨ Thank you for ordering from Murf Coffee Shop! ✨
            </p>
        </div>
        </body>
        </html>
        """
        
        return html


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly and enthusiastic barista at Murf Coffee Shop, the finest coffee establishment in town. 
            The user is interacting with you via voice, even if you perceive the conversation as text.
            
            Your job is to take customer orders in a warm and welcoming manner. You should:
            - Greet customers cheerfully
            - Ask about their drink preferences one at a time
            - Confirm their choices enthusiastically
            - Make suggestions when appropriate
            - Keep your responses conversational and brief
            - Never use complex formatting, emojis, asterisks, or other symbols
            
            You need to collect the following information for each order:
            1. Drink type (e.g., latte, cappuccino, espresso, americano, mocha, flat white)
            2. Size (small, medium, or large)
            3. Milk type (whole milk, skim milk, oat milk, almond milk, soy milk, or no milk)
            4. Any extras (e.g., extra shot, vanilla syrup, caramel drizzle, whipped cream, chocolate chips)
            5. Customer's name
            
            Once you have all the information, use the save_order tool to finalize the order and thank the customer warmly.""",
        )
        self.current_order = CoffeeOrder()
        self._room = None
    
    def set_room(self, room):
        """Store reference to the LiveKit room for data publishing."""
        self._room = room

    @function_tool
    async def save_order(self, context: RunContext):
        """Use this tool to save the completed coffee order to a JSON file.
        
        Only call this tool when you have collected ALL required information:
        - drink type
        - size
        - milk type
        - customer name
        
        The extras field is optional and can be an empty list.
        """
        if not self.current_order.is_complete():
            missing = []
            if not self.current_order.drink_type:
                missing.append("drink type")
            if not self.current_order.size:
                missing.append("size")
            if not self.current_order.milk:
                missing.append("milk type")
            if not self.current_order.name:
                missing.append("customer name")
            return f"Cannot save order yet. Still need: {', '.join(missing)}"
        
        # Create orders directory if it doesn't exist
        orders_dir = Path("orders")
        orders_dir.mkdir(exist_ok=True)
        
        # Generate filename with customer name and timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.current_order.name}_{timestamp}.json"
        filepath = orders_dir / filename
        
        # Save order to JSON file
        with open(filepath, 'w') as f:
            json.dump(self.current_order.to_dict(), f, indent=2)
        
        logger.info(f"Order saved to {filepath}")
        
        # Generate HTML visualization
        html_content = self.current_order.generate_beverage_html()
        
        # Delay publishing visualization to allow agent to finish speaking completely
        # This ensures the receipt appears AFTER the agent says "thank you" and everything is done
        async def publish_with_delay():
            await asyncio.sleep(18)  # Wait 18 seconds for agent to finish completely
            try:
                if self._room:
                    await self._room.local_participant.publish_data(
                        html_content.encode('utf-8'),
                        topic="order-visualization"
                    )
                    logger.info("Published order visualization to frontend")
                else:
                    logger.error("Room not available for publishing visualization")
            except Exception as e:
                logger.error(f"Failed to publish visualization: {e}")
        
        # Schedule the delayed publication as a background task
        asyncio.create_task(publish_with_delay())
        
        return f"Perfect! Your order has been saved successfully. Order summary: {self.current_order.size} {self.current_order.drink_type} with {self.current_order.milk}, extras: {', '.join(self.current_order.extras) if self.current_order.extras else 'none'}, for {self.current_order.name}. Your delicious coffee will be ready shortly!"

    @function_tool
    async def set_drink_type(self, context: RunContext, drink_type: str):
        """Set the type of drink the customer wants to order.
        
        Args:
            drink_type: The type of coffee drink (e.g., latte, cappuccino, espresso, americano, mocha, flat white)
        """
        self.current_order.drink_type = drink_type.lower()
        logger.info(f"Set drink type to: {drink_type}")
        return f"Great choice! A {drink_type} it is."

    @function_tool
    async def set_size(self, context: RunContext, size: str):
        """Set the size of the drink.
        
        Args:
            size: The size of the drink (small, medium, or large)
        """
        size_lower = size.lower()
        if size_lower not in ["small", "medium", "large"]:
            return "Sorry, we only have small, medium, or large sizes available."
        
        self.current_order.size = size_lower
        logger.info(f"Set size to: {size}")
        return f"Got it! {size} size."

    @function_tool
    async def set_milk(self, context: RunContext, milk_type: str):
        """Set the type of milk for the drink.
        
        Args:
            milk_type: The type of milk (whole milk, skim milk, oat milk, almond milk, soy milk, or no milk)
        """
        self.current_order.milk = milk_type.lower()
        logger.info(f"Set milk to: {milk_type}")
        return f"Perfect! {milk_type} noted."

    @function_tool
    async def add_extra(self, context: RunContext, extra: str):
        """Add an extra item to the drink order (e.g., extra shot, syrup, whipped cream).
        
        Args:
            extra: The extra item to add to the drink
        """
        extra_lower = extra.lower()
        # Only add if not already in extras to prevent duplicates
        if extra_lower not in self.current_order.extras:
            self.current_order.extras.append(extra_lower)
            logger.info(f"Added extra: {extra}")
            return f"Added {extra} to your order!"
        else:
            logger.info(f"Extra already in order: {extra}")
            return f"{extra} is already in your order!"

    @function_tool
    async def set_customer_name(self, context: RunContext, name: str):
        """Set the customer's name for the order.
        
        Args:
            name: The customer's name
        """
        self.current_order.name = name
        logger.info(f"Set customer name to: {name}")
        return f"Thanks {name}!"


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

    # Create assistant instance and give it access to the room
    assistant = Assistant()
    assistant.set_room(ctx.room)
    
    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=assistant,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
