import React from 'react';
import { Box } from '@chakra-ui/react';

// Convert plain text to HTML
const convertTextToHTML = (text) => {
  // Replace headers
  let html = text.replace(/(\*\*[^*]+\*\*)/g, '<h2>$1</h2>');

  // Replace bullet points
  html = html.replace(/(\* [^\n]+)/g, '<li>$1</li>');

  // Wrap bullet points with <ul>
  html = html.replace(/(<li>.*?<\/li>)/g, '<ul>$1</ul>');

  // Replace bold text
  html = html.replace(/\*\*([^\*]+)\*\*/g, '<b>$1</b>');

  return html;
};

const MessageBox = ({ message, index }) => {
  const htmlContent = convertTextToHTML(message.text); // Convert text to HTML

  return (
    <Box
      p='2'
      mb='2'
      borderRadius='md'
      bg={message.type === 'sent' ? 'blue.100' : 'gray.100'}
      alignSelf={message.type === 'sent' ? 'flex-end' : 'flex-start'} // Align based on message type
      maxW='70%'
      textAlign="left"
      key={index}
      fontFamily='Times New Roman'
      ml={message.type === 'sent' ? 'auto' : '0'} // Margin based on message type
      whiteSpace='pre-wrap' // Preserve whitespace and line breaks
      dangerouslySetInnerHTML={{ __html: htmlContent }} // Render HTML content
    />
  );
};

export default MessageBox;
