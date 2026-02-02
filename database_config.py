"""
Database configuration for chat history storage
"""
import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
from typing import List, Dict, Optional

class ChatDatabase:
    def __init__(self, host="localhost", user="root", password="", database="jarvis_chatbot"):
        """
        Initialize database connection
        
        Args:
            host: Database host (default: localhost)
            user: Database user (default: root)
            password: Database password (default: empty for XAMPP)
            database: Database name
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Successfully connected to database")
                return True
        except Error as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed")
    
    def create_session(self, session_id: str, model_type: str, title: str = None) -> bool:
        """
        Create a new chat session
        
        Args:
            session_id: Unique session identifier
            model_type: Type of model (llama, qwen, gemini)
            title: Optional session title
        
        Returns:
            bool: Success status
        """
        try:
            cursor = self.connection.cursor()
            
            # Generate title from first message if not provided
            if not title:
                title = f"Chat with {model_type.capitalize()}"
            
            query = """
                INSERT INTO chat_sessions (session_id, model_type, title)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE updated_at = CURRENT_TIMESTAMP
            """
            cursor.execute(query, (session_id, model_type, title))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error creating session: {e}")
            return False
    
    def save_message(self, session_id: str, role: str, content: str, 
                    model_type: str = None, sources: List[str] = None, 
                    suggested_questions: List[str] = None) -> bool:
        """
        Save a chat message to database
        
        Args:
            session_id: Session identifier
            role: Message role (user, assistant, system)
            content: Message content
            model_type: Model used for response
            sources: List of source documents (optional)
            suggested_questions: List of suggested follow-up questions (optional)
        
        Returns:
            bool: Success status
        """
        try:
            cursor = self.connection.cursor()
            
            # Convert lists to JSON strings
            sources_json = json.dumps(sources) if sources else None
            questions_json = json.dumps(suggested_questions) if suggested_questions else None
            
            query = """
                INSERT INTO chat_messages 
                (session_id, role, content, model_type, sources, suggested_questions)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (session_id, role, content, model_type, 
                                  sources_json, questions_json))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error saving message: {e}")
            return False
    
    def get_session_messages(self, session_id: str) -> List[Dict]:
        """
        Retrieve all messages from a session
        
        Args:
            session_id: Session identifier
        
        Returns:
            List of message dictionaries
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT id, role, content, model_type, sources, suggested_questions, created_at
                FROM chat_messages
                WHERE session_id = %s
                ORDER BY created_at ASC
            """
            cursor.execute(query, (session_id,))
            messages = cursor.fetchall()
            cursor.close()
            
            # Parse JSON fields
            for msg in messages:
                msg['sources'] = json.loads(msg['sources']) if msg['sources'] else []
                msg['suggested_questions'] = json.loads(msg['suggested_questions']) if msg['suggested_questions'] else []
                msg['timestamp'] = msg['created_at'].isoformat() if msg['created_at'] else None
            
            return messages
        except Error as e:
            print(f"Error retrieving messages: {e}")
            return []
    
    def get_all_sessions(self, limit: int = 50) -> List[Dict]:
        """
        Retrieve all chat sessions with preview
        
        Args:
            limit: Maximum number of sessions to retrieve
        
        Returns:
            List of session dictionaries with preview
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """
                SELECT 
                    s.session_id,
                    s.model_type,
                    s.title,
                    s.created_at,
                    s.updated_at,
                    (SELECT content FROM chat_messages 
                     WHERE session_id = s.session_id AND role = 'user'
                     ORDER BY created_at ASC LIMIT 1) as first_message,
                    (SELECT COUNT(*) FROM chat_messages 
                     WHERE session_id = s.session_id) as message_count
                FROM chat_sessions s
                ORDER BY s.updated_at DESC
                LIMIT %s
            """
            cursor.execute(query, (limit,))
            sessions = cursor.fetchall()
            cursor.close()
            
            # Format dates
            for session in sessions:
                session['created_at'] = session['created_at'].isoformat() if session['created_at'] else None
                session['updated_at'] = session['updated_at'].isoformat() if session['updated_at'] else None
                
                # Generate title from first message if title is generic
                if session['first_message'] and (not session['title'] or 'Chat with' in session['title']):
                    session['title'] = session['first_message'][:50] + ('...' if len(session['first_message']) > 50 else '')
            
            return sessions
        except Error as e:
            print(f"Error retrieving sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a chat session and all its messages
        
        Args:
            session_id: Session identifier
        
        Returns:
            bool: Success status
        """
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM chat_sessions WHERE session_id = %s"
            cursor.execute(query, (session_id,))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error deleting session: {e}")
            return False
    
    def update_session_title(self, session_id: str, title: str) -> bool:
        """
        Update session title
        
        Args:
            session_id: Session identifier
            title: New title
        
        Returns:
            bool: Success status
        """
        try:
            cursor = self.connection.cursor()
            query = "UPDATE chat_sessions SET title = %s WHERE session_id = %s"
            cursor.execute(query, (title, session_id))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error updating title: {e}")
            return False
