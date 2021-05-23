import React from "react"

class Table extends React.Component {
    render () {
       const data = this.props.tableData.data
       return (
        <div className="my-table">
            <h1>Result</h1>
            <table>
                <thead>
                <tr>
                    <th>Number</th>
                    <th>Document name</th>
                    <th>Raw text</th>
                </tr>
                </thead>
                <tbody>
                     {
                        data.map((item) => (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.doc}</td>
                                <td>{item.link}</td>
                                <td/>
                            </tr>
                        ))
                    }
                </tbody>
            </table>
        </div>
       )
    }
}

export default Table