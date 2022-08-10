import logo from './logo.svg';
import './App.css';
import DataTable from 'react-data-table-component-with-filter';
import {useEffect, useState} from 'react';
import {ClipLoader} from 'react-spinners'

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);

  const url = "./output.json"
  useEffect(() => {
    setLoading(true);
    fetch(url)
      .then(data => data.json())
      .then(data => {
        console.log(data);
        const data2 = data.sort( (a,b)=>b.pmid > a.pmid)
        setData(data2);
        setLoading(false);
      })
    }, [])


const columns = [
    {
   
        name: 'Title',
       // selector creates HTML link
        selector: 'title',
        // set width to 50%:
        minWidth: "40%",
        sortable: true,
        filterable: true,
        cell: row => <a href={"https://pubmed.ncbi.nlm.nih.gov/"+row.pmid} style={
          {
            color: 'black',
            textDecoration: 'none',
          }
        }>{row.title}</a>
    },
    {
        name: 'PMID',
        selector: 'pmid',
        sortable: true,
        filterable: true
    },
    {
      name: 'Phenotype confidence',
      selector: 'pheno_conf',
      sortable: true,
      cell: row => <>{row.pheno_conf}%</>
  },
    {
        name: 'Organism',
        selector: 'organism',
        sortable: true,
        filterable: true
    },
    {
        name: 'Organism confidence',
        selector: 'org_conf',
        sortable: true,
        cell: row => <>{row.org_conf}%</>

    },

];



    return (<>
    <h2>Plasmodium phenotype papers</h2>
    {(loading ? 
    <ClipLoader /> : 
    
        <DataTable
            columns={columns}
            data={data}
            direction="auto"
           
            pagination
            responsive
            defaultSortFieldId={2}
            defaultSortAsc = {false}
           
            
        />)}
        </>
    );


}

export default App;
