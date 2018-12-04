'use strict';

class Queries extends React.Component {
  render() {
    return (
      <div>
        <label htmlFor="query">Type</label>
        <select id="query" onChange={this.props.selectQuery.bind(this)} className="form-control mb-3">
          <option key="none">select</option>
          {this.props.queries.map(query => (
            <option key={query.name}>{query.name}</option>
          ))}
        </select>
      </div>
    );
  }
}

class QueryParameters extends React.Component {
  render() {
    return (
      <div>
        <label htmlFor="parameters">Parameters</label>
        <div id="parameters">
          {this.props.query.parameters.map((parameter, index) => (
            <div key={index}>
              <div className="input-group mb-3">
                <div className="input-group-prepend">
                  <span className="input-group-text">{parameter.name}</span>
                </div>
                <select onChange={this.props.selectQueryParameter.bind(null, index)} className="custom-select">
                  <option key="all">all</option>
                  {parameter.values.map(value => (
                    <option key={value.name}>{value.name}</option>
                  ))}
                </select>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

class QueryFields extends React.Component {
  render() {
    return (
      <div>
        <label htmlFor="test">Fields</label>
        <div id="fields">
          {this.props.query.fields.map((field, index) => (
            <div className="form-check form-check-inline mb-3" key={field.name}>
              <input onChange={this.props.selectQueryFields.bind(null, index)}
                className="form-check-input" type="checkbox" checked={field.selected} id={'fields'+index}/>
              <label className="form-check-label" htmlFor={'fields'+index}>{field.name}</label>
            </div>
          ))}
        </div>
      </div>
    );
  }
}

class Results extends React.Component {
  render() {
    const fields = this.props.query.fields.filter(field => field.selected);
    return (
      <div>
        <h4>Results</h4>
        <table className="table">
          <thead>
            <tr>
              {fields.map((field, index) => (
                <th key={index} scope="col">{field.name}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {this.props.results.map((item, index) => (
              <tr key={index}>
                {fields.map((field, index) => (
                  <td key={index}>{item[field.name]}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }
}


class App extends React.Component {
  constructor(props) {
    super(props);
    this.url =  "https://us-central1-sheeking-shelter-8443b.cloudfunctions.net/api/graphql";
    this.state = {
      loading: true,
      queries: null,
      selectedQuery: null,
      queryString: null,
      results: null
    };
  }

  componentDidMount() {
    this.fetchApiMetadata();
  }

  onSelectQuery(event) {
    const selectedQuery = this.state.queries[event.target.selectedIndex - 1];
    const queryString = this.writeQuery(selectedQuery);
    this.setState({
      selectedQuery: selectedQuery,
      queryString: queryString,
      loading: true
    }, () => this.executeQuery());

  }

  onSelectQueryParameter(parameterIndex, event) {
    const selectedQuery = this.state.selectedQuery;
    const value = selectedQuery.parameters[parameterIndex].values[event.target.selectedIndex - 1].name;
    selectedQuery.parameters[parameterIndex].selectedValue = value;
    const queryString = this.writeQuery(selectedQuery);
    this.setState({
      selectedQuery: selectedQuery,
      queryString: queryString,
      loading: true
    }, () => this.executeQuery());
  }

  onSelectQueryFields(index, event) {
    const activate = event.target.checked;
    const selectedQuery = this.state.selectedQuery;
    selectedQuery.fields[index].selected = activate;
    const queryString = this.writeQuery(selectedQuery);
    this.setState({
      selectedQuery: selectedQuery,
      queryString: queryString,
      loading: activate
    }, () => {
      if (activate) {
        this.executeQuery();
      }
    });
  }

  fetchApiMetadata() {
    axios.post(this.url, {
      query: `
      {
        __type(name: "Query") {
          name
          fields {
            name
            type {
              ofType {
                ofType {
                  ofType {
                    name
                    fields {
                      name
                    }
                  }
                }
              }
            }
            args {
              name
              type {
                name
                enumValues {
                  name
                }
              }
            }
          }
        }
      }
      `
    })
    .then(response => {
      const queries = response.data.data.__type.fields.map(query => ({
        name: query.name,
        parameters: query.args.map(arg => ({
          name: arg.name,
          values: arg.type.enumValues.map(value => ({
            name: value.name
          }))
        })),
        fields: query.type.ofType.ofType.ofType.fields.map(field => ({
          name: field.name,
          selected: true
        }))
      }));
      this.setState({
        loading: false,
        queries: queries
      })
    })
    .catch(error => {
      console.log(error);
    })
  }

  writeQuery(query) {
    const parameters = query.parameters.filter(parameter => parameter.selectedValue);
    const parameterString = parameters.length ?
    `(${parameters.map(parameter => `${parameter.name}: ${parameter.selectedValue}`).join(',')})`
    : '';
    const fieldsString = query.fields.filter(field => field.selected).map(field => field.name).join('\n');
    const queryString = `
    query {
      ${query.name}${parameterString} {
        ${fieldsString}
      }
    }
    `;
    return queryString;
  }

  executeQuery() {
    this.setState({
      results: null,
      loading: true
    });
    axios.post(this.url, {
      query: this.state.queryString
    })
    .then(response => {
      this.setState({
        loading: false,
        results: response.data.data[this.state.selectedQuery.name]
      })
    })
    .catch(error => console.log(error));
  }

  render() {
    const { loading, queries, selectedQuery, results } = this.state;
    return (
      <div>
        <h4>Query</h4>
        {queries ?
          <Queries queries={queries} selectQuery={this.onSelectQuery.bind(this)}/>
          : <p>Loading query metadata...</p>
      }
      {selectedQuery &&
        <div>
          <QueryParameters query={selectedQuery} selectQueryParameter={this.onSelectQueryParameter.bind(this)}/>
          <QueryFields query={selectedQuery} selectQueryFields={this.onSelectQueryFields.bind(this)}/>
        </div>
      }
      {results &&
        <Results query={selectedQuery} results={results}/>
      }
      {loading &&
        <div className="progress">
          <div className="progress-bar progress-bar-striped progress-bar-animated" role="progressbar" style={{width: '100%'}}></div>
        </div>
      }
    </div>
  );
}
}

const domContainer = document.querySelector('#app');
ReactDOM.render(<App/>, domContainer);
