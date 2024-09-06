import { Route, Router, Routes } from 'react-router-dom';
import './App.css';
import UploadArea from './Components/UploadArea';
import ChatArea from './Components/PdfChatArea';
import SqlChatArea from './Components/SqlChatArea';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path  = '/' element = {<UploadArea/>}></Route>
        <Route path  = '/chat_pdf' element = {<ChatArea/>}></Route>
        <Route path  = '/chat_sql' element = {<SqlChatArea/>}></Route>
      </Routes>
    </div>
  );
}

export default App;
