import React from "react"
import DocumentTable from "./Table"
import { Button, Form, Navbar, Alert } from "react-bootstrap"
import "./App.css";

class MyForm extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            querry: "",
            documents: [],
            ids: [],
            links: [],
            time: 0.0,
            querryVisible: false,
            recordVisible: false
        }
    }

    handleSubmit = (event) => {
        event.preventDefault()
        this.setState({documents: [], ids: [], links: [], querryVisible:false, recordVisible:false})
        const documents = this.state
        console.log(documents)
        const options = {
            method: 'POST',
            mode: 'cors',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({querry: documents,})
        }

        fetch('http://localhost:5000/querry', options)
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw response
            }
        })
        .then(data => { const documents = data.table;
                        const ids = data.ids;
                        const links = data.links
                        console.log(data.table)
                        if ( documents.length === 0 ){
                            this.setState({recordVisible: true})
                        }
                        this.setState({documents: documents, ids: ids, links: links})})
        .catch(error => { error.text().then( errMessage => { 
                          this.setState({querryVisible: true})  
                          console.log(errMessage) }) })
    }
            
    
    handleInputChagne = (event) => {
        event.preventDefault()
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    render () {
        const {querry} = this.state
        const {documents} = this.state
        const {ids} = this.state
        const {links} = this.state
        
        var data = [];
        var jsonData = {};

        for (var i = 0; i < documents.length; i++) 
        { 
            data.push({ 
                "doc" : documents[i],
                "id"  : ids[i],
                "link" : links[i] 
            });
        }

        jsonData.data = data;
        
        return (
        <div>
        <Navbar bg="light" style={{marginLeft: "20px"}}>
         <Navbar.Brand>Boolean model</Navbar.Brand>
        </Navbar>
        <Form onSubmit={this.handleSubmit} style={{width:"60%", marginLeft:"20%", marginTop:"10%"}}>
            <Form.Group controlId="formBasicEmail">
            <Form.Control size="lg" type="text" placeholder="Enter boolean querry"
                          value={querry} name='querry' margin="normal" onChange={this.handleInputChagne} />  
            </Form.Group>
            <br/>
            <p><Button style={{width:"20%"}}variant="primary" type="submit">Evaluate</Button></p>
        </Form>
        <p></p>
        <Alert className={this.state.querryVisible?'fadeIn':'fadeOut'} variant="danger">Not a valid boolean querry!</Alert>
        <Alert className={this.state.recordVisible?'fadeIn':'fadeOut'} variant="primary">No documments found</Alert>
        <DocumentTable tableData={jsonData}></DocumentTable>
        </div>
    )
    }
}

export default MyForm