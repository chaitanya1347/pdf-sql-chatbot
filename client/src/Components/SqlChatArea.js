import React, { useEffect, useState, useRef } from 'react';
import { Box, Grid, GridItem, Input, OrderedList, ListItem, Spinner, VStack, Progress } from '@chakra-ui/react';
import axios from 'axios';
import MessageBox from './MessageBox';
import { Skeleton, SkeletonCircle, SkeletonText } from '@chakra-ui/react'

function SqlChatArea() {
  const [files, setFiles] = useState([{"Key":"db.sqlite"}]);
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState([{ text: "Hi How can I assist you today!", type: "received" }]);
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);



  useEffect(() => {
    // Scroll to the bottom whenever messages change
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  const handleKeyDown = async (e) => {
    if (e.key === 'Enter' && query.trim() !== '') {
      try {
        const newMessage = { text: query, type: 'sent' };
        setMessages(prevMessages => [...prevMessages, newMessage]);
        setQuery(''); // Clear the input field after submission
        setLoading(true);

        const result = await axios.get(`http://localhost:8000/ask_sql_query?question=${encodeURIComponent(query)}`);
        const botReply = { text: result.data.answer || 'No response from the server', type: 'received' };

        setMessages(prevMessages => [...prevMessages, botReply]);
        setLoading(false);
      } catch (error) {
        console.log("Error asking query:", error);
        setLoading(false);
      }
    }
  };


  return (
    <div className='container'>
      <Grid
        templateAreas={"\"header header\" \"nav main\" \"nav footer\""}
        gridTemplateRows={'50px 1fr 35px'}
        gridTemplateColumns={'25% 72%'}
        h='40rem' gap='3' color='blackAlpha.700' fontWeight='bold'
      >
        <GridItem area={'header'}>
          <div className='heading-chat-area'>
            <h2>Welcome to the Chat Area</h2>
          </div>
        </GridItem>

        <GridItem
          pl='0'
          area={'nav'}
          bg='gray.100'
          borderRadius='md'
          boxShadow='sm'
        >
          <div className='heading-chat-area'>
            All the files that you have uploaded
          </div>
          <div className='document-list'>
            <OrderedList>
              {files.map((file, index) => (
                <ListItem key={index} className='file-name'>
                  {file["Key"]}
                </ListItem>
              ))}
            </OrderedList>
          </div>
        </GridItem>

        <GridItem
          pl='5'
          area={'main'}
          bg='white'
          borderRadius='md'
          boxShadow='sm'
          overflowY='auto'
          p={4}
          className='message-container'
        >
          <VStack spacing={4} align='start'>
            {messages.map((msg, index) => (
              <MessageBox message={msg} index={index} key={index} />
            ))}
            {loading &&<Skeleton width = '500px'>
                        <div>contents wrapped</div>
                         <div>won't be visible</div>
                        </Skeleton>
            }
            <div ref={messagesEndRef} /> {/* This element helps to scroll to the bottom */}
          </VStack>
        </GridItem>

        <GridItem
          area={'footer'}
          bg='gray.100'
          borderRadius='md'
          boxShadow='sm'
        >
          <Input
            size='md'
            placeholder='Ask Whatever you want'
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
          />
        </GridItem>
      </Grid>
    </div>
  );
}

export default SqlChatArea;
