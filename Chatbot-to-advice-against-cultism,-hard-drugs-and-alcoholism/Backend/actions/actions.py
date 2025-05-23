# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import logging

logger = logging.getLogger(__name__)

class ActionAssessEmergencyLevel(Action):
    """Assess the emergency level based on user's situation"""
    
    def name(self) -> Text:
        return "action_assess_emergency_level"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        latest_intent = tracker.latest_message['intent']['name']
        latest_text = tracker.latest_message.get('text', '').lower()
        
        # High-risk keywords that indicate immediate danger
        critical_keywords = [
            'threatened', 'threatening', 'violence', 'hurt', 'harm', 
            'danger', 'scared', 'afraid', 'suicidal', 'kill', 'die',
            'overdose', 'unconscious', 'emergency'
        ]
        
        high_risk_keywords = [
            'can\'t stop', 'addicted', 'daily', 'everyday', 'blackout',
            'withdrawal', 'dependency', 'controlling my life'
        ]
        
        medium_risk_keywords = [
            'pressure', 'forced', 'peer pressure', 'family worried',
            'grades affected', 'relationship problems'
        ]
        
        # Determine emergency level
        emergency_level = "low"
        
        if latest_intent == "emergency" or any(word in latest_text for word in critical_keywords):
            emergency_level = "critical"
        elif (latest_intent in ["alcohol_problem", "drug_problem", "cultism_escape"] 
              or any(word in latest_text for word in high_risk_keywords)):
            emergency_level = "high"
        elif (latest_intent in ["alcohol_pressure", "drug_pressure", "cultism_pressure", "family_concerns"]
              or any(word in latest_text for word in medium_risk_keywords)):
            emergency_level = "medium"
        
        # Set appropriate help needed flag
        help_needed = emergency_level in ["high", "critical"]
        
        return [
            SlotSet("emergency_level", emergency_level),
            SlotSet("help_needed", help_needed)
        ]

class ActionProvideResources(Action):
    """Provide appropriate resources based on the user's situation"""
    
    def name(self) -> Text:
        return "action_provide_resources"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        emergency_level = tracker.get_slot("emergency_level")
        latest_intent = tracker.latest_message['intent']['name']
        
        # Determine current issue type
        current_issue = "general"
        if latest_intent.startswith("cultism"):
            current_issue = "cultism"
        elif latest_intent.startswith("alcohol"):
            current_issue = "alcohol"
        elif latest_intent.startswith("drug"):
            current_issue = "drugs"
        
        # Provide resources based on emergency level and issue type
        if emergency_level == "critical":
            message = """🚨 **IMMEDIATE EMERGENCY RESOURCES** 🚨
            
**Call NOW:**
• Emergency Services: 911
• Crisis Text Line: Text HOME to 741741
• National Suicide Prevention Lifeline: 988
• Campus Security: [Insert your campus number]

**24/7 Helplines:**
• SAMHSA National Helpline: 1-800-662-4357
• Crisis Chat: suicidepreventionlifeline.org

⚠️ **If you're in immediate danger, call 911 immediately!**"""

        elif emergency_level == "high":
            if current_issue == "cultism":
                message = """🆘 **URGENT CULTISM RESOURCES**
                
**Immediate Help:**
• Campus Security: [Insert number]
• Student Affairs Office: [Insert number]
• Local Police Non-Emergency: [Insert number]
• Campus Counseling Center: [Insert number]

**National Resources:**
• FBI Tips: tips.fbi.gov
• SAMHSA Helpline: 1-800-662-4357

**Safety Planning:**
• Document any threats or evidence
• Stay in public areas
• Inform trusted friends/family of your location"""

            elif current_issue == "alcohol":
                message = """🆘 **ALCOHOL ADDICTION RESOURCES**
                
**Treatment Centers:**
• Campus Health Services: [Insert number]
• Local AA Meetings: aa.org
• SAMHSA Treatment Locator: findtreatment.gov

**24/7 Support:**
• SAMHSA Helpline: 1-800-662-4357
• Crisis Text Line: Text HOME to 741741

**Campus Resources:**
• Counseling Center: [Insert number]
• Student Health Center: [Insert number]
• Academic Advisor: [Insert number]"""

            elif current_issue == "drugs":
                message = """🆘 **DRUG ADDICTION RESOURCES**
                
**Immediate Treatment:**
• SAMHSA Treatment Locator: findtreatment.gov
• Local Detox Centers: [Insert local numbers]
• Campus Health Emergency: [Insert number]

**Support Groups:**
• Narcotics Anonymous: na.org
• SMART Recovery: smartrecovery.org
• Crystal Meth Anonymous: crystalmeth.org

**24/7 Helplines:**
• SAMHSA: 1-800-662-4357
• Poison Control: 1-800-222-1222"""

        elif emergency_level == "medium":
            message = f"""📞 **SUPPORT RESOURCES FOR {current_issue.upper()} CONCERNS**
            
**Campus Support:**
• Counseling Center: [09034499670]
• Student Affairs: [09034499670]
• Academic Advising: [09034499670]
• Peer Support Groups: [Ncf - 09034499670]

**Community Resources:**
• Local Support Groups
• Community Mental Health Centers
• Religious/Spiritual Counselors
• Youth Organizations

**Online Resources:**
• Campus website resources
• Mental health apps
• Educational materials
• Peer support forums"""

        else:  # Low risk
            message = """📚 **EDUCATIONAL & PREVENTION RESOURCES**
            
**Learning Materials:**
• Campus health education programs
• Online courses on substance abuse
• Peer education workshops
• Health fair information

**Positive Activities:**
• Student clubs and organizations
• Intramural sports
• Volunteer opportunities
• Academic study groups

**Wellness Resources:**
• Campus recreation center
• Counseling for general wellness
• Stress management workshops
• Healthy lifestyle programs"""

        dispatcher.utter_message(text=message)
        
        # Additional personalized message based on situation
        if emergency_level in ["critical", "high"]:
            dispatcher.utter_message(
                text="Remember: Seeking help is a sign of strength, not weakness. "
                     "You don't have to face this alone. Professional help is available "
                     "and recovery is possible."
            )
        
        return [SlotSet("current_issue", current_issue)]

class ActionScheduleFollowup(Action):
    """Schedule follow-up support for the user"""
    
    def name(self) -> Text:
        return "action_schedule_followup"
    
    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        emergency_level = tracker.get_slot("emergency_level")
        current_issue = tracker.get_slot("current_issue")
        
        if emergency_level in ["critical", "high"]:
            message = """📅 **FOLLOW-UP SUPPORT PLAN**
            
**Immediate Next Steps:**
1. Contact one of the resources provided within 24 hours
2. Reach out to a trusted friend or family member today
3. Remove access to harmful substances/situations
4. Return here anytime you need support

**This Week:**
• Schedule appointment with counselor
• Attend support group meeting
• Connect with campus resources
• Create safety plan

**Ongoing Support:**
• Regular check-ins with counselor
• Maintain connection with support network
• Continue using healthy coping strategies
• Monitor your progress and celebrate small victories

💪 **Remember:** Recovery is a process, not a single event. Each step forward matters."""

        else:
            message = """📋 **PREVENTION & WELLNESS PLAN**
            
**This Week:**
• Explore one new healthy activity
• Connect with positive peer groups
• Practice refusal skills if needed
• Review campus resources available

**Monthly Goals:**
• Join a club or organization
• Maintain good academic standing
• Build strong, healthy relationships
• Continue learning about these issues

**Always Remember:**
• You have the power to make good choices
• It's okay to ask for help when you need it
• Your future is worth protecting
• Small positive changes make a big difference"""

        dispatcher.utter_message(text=message)
        
        return []