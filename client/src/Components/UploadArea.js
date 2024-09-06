import React, { useEffect, useState } from 'react';
import { Box, Container, Heading, Spinner, Alert, AlertIcon, AlertTitle, AlertDescription, useToast } from '@chakra-ui/react';
import '../static/style.css';
import myImage from '../static/upload_document_pdf.png';
import myImage2 from '../static/upload_document_sql.png';
import axios from "axios";
import { useNavigate } from 'react-router-dom';

function UploadArea() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [fileType, setFileType] = useState(null);
    const toast = useToast();
    const navigate = useNavigate();

    useEffect(() => {
        if (files.length > 0) {
            handleUpload();
        }
    }, [files]);

    const handleFileChange = (event, type) => {
        setFileType(type);
        setFiles(event.target.files);
    };

    const handleUpload = async () => {
        setLoading(true);
        setError(null);
        try {
            for (let i = 0; i < files.length; i++) {
                const formData = new FormData();   
                formData.append('file', files[i]);
                formData.append('fileType', fileType);

                const { data } = await axios.post("http://localhost:8000/uploadFiles", formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            }
            let fileName = "";
            for (let i = 0; i < files.length; i++) {
                fileName += files[i].name;
                if(i!==files.length - 1) fileName += ","
            }
            toast({ title: 'Files Uploaded successfully.', status: 'success', duration: 2000, isClosable: true });
            fileType === 'pdf' ? navigate('/chat_pdf',{state:{fileName}}) : navigate('/chat_sql');
            setFileType(null)
            
        } catch (error) {
            console.error(error.message);
            setError(error.message);
        } finally {
            setLoading(false);
        }   
    };

    useEffect(() => {
        if (error) {
            const timeout = setTimeout(() => {
                setError(null); 
            }, 2000); 
            return () => clearTimeout(timeout); 
        }
    }, [error]);

    return (
        <div className='container'>
            <div className='header'>
                <Heading>Chat with your files</Heading>
            </div>
            <div className='desc-upload'>
                Upload a PDF document and SQL file to get your queries answered by an interactive chatbot.
            </div>

            <Container maxW="xl" centerContent>
                <Box
                    as="label"
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    p={3}
                    bg="white"
                    w="700px"
                    h="150px"
                    m="40px 0 15px 0"
                    borderRadius="lg"
                    borderWidth="1px"
                    userSelect="none"
                    _hover={{ cursor: 'pointer' }}
                >
                    <input
                        type="file"
                        multiple
                        style={{ display: 'none' }}
                        onChange={(e) => handleFileChange(e, "pdf")}
                    />
                    <img
                        src={myImage}
                        alt="Upload Files"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                </Box>
            </Container>

            {loading && (
                <Spinner
                    thickness='4px'
                    speed='0.65s'
                    emptyColor='gray.200'
                    color='blue.500'
                    size='xl'
                    marginTop="20px"
                />
            )}
            <Container maxW="xl" centerContent>
                <Box
                    as="label"
                    display="flex"
                    justifyContent="center"
                    alignItems="center"
                    p={3}
                    bg="white"
                    w="700px"
                    h="150px"
                    m="40px 0 15px 0"
                    borderRadius="lg"
                    borderWidth="1px"
                    userSelect="none"
                    _hover={{ cursor: 'pointer' }}
                >
                    <input
                        type="file"
                        multiple
                        style={{ display: 'none' }}
                        onChange={(e) => handleFileChange(e, "sql")}
                    />
                    <img
                        src={myImage2}
                        alt="Upload Files"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                </Box>
            </Container>

            {error && (
                <Alert status='error' marginTop="20px">
                    <AlertIcon />
                    <AlertTitle>Error!</AlertTitle>
                    <AlertDescription>{error}</AlertDescription>
                </Alert>
            )}
           
        </div>
    );
}

export default UploadArea;
