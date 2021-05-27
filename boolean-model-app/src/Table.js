import React from "react"
import { withStyles } from '@material-ui/core/styles';
import "bootstrap/dist/css/bootstrap.min.css"
import { Table } from "react-bootstrap"

const useStyles = theme => ({
    table: {
    
    },
});

class DocumentTable extends React.Component {
    render () {
       const data = this.props.tableData.data
       return (
            <Table striped bordered hover style={{marginLeft: "20%", marginTop: "100px", width:"60%"}} >
                <thead>
                <tr>
                    <th>#</th>
                    <th>Document name</th>
                    <th>Link to raw text</th>
                </tr>
                </thead>
                <tbody>
                     {
                        data.map((item) => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.doc}</td>
                                <td>{item.link}</td>
                            </tr>
                        ))
                    }
                </tbody>
            </Table>
            
       )
    }
}

export default withStyles(useStyles)(DocumentTable)