import React from "react"
import Table from "./Table"

class Form extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            querry: "",
            documents: [],
            ids: [],
            links: []
        }
    }

    handleSubmit = (event) => {
        event.preventDefault()
        const documents = this.state

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

                        this.setState({documents: documents, ids: ids, links: links})})
        .catch(error => { error.text().then( errMessage => { console.log(errMessage) }) })
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
        <h1>Boolean model</h1>
        <form onSubmit={this.handleSubmit}>
            <p><input type='text' placeholder='your boolean querry' value={querry} name='querry' onChange={this.handleInputChagne}></input></p>
            <p><button>Evaluate querry</button></p>
        </form>

        <Table tableData={jsonData}></Table>
        </div>
    )
    }
}

export default Form