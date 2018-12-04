'use strict';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

var Queries = function (_React$Component) {
  _inherits(Queries, _React$Component);

  function Queries() {
    _classCallCheck(this, Queries);

    return _possibleConstructorReturn(this, (Queries.__proto__ || Object.getPrototypeOf(Queries)).apply(this, arguments));
  }

  _createClass(Queries, [{
    key: "render",
    value: function render() {
      return React.createElement(
        "div",
        null,
        React.createElement(
          "label",
          { htmlFor: "query" },
          "Type"
        ),
        React.createElement(
          "select",
          { id: "query", onChange: this.props.selectQuery.bind(this), className: "form-control mb-3" },
          React.createElement(
            "option",
            { key: "none" },
            "select"
          ),
          this.props.queries.map(function (query) {
            return React.createElement(
              "option",
              { key: query.name },
              query.name
            );
          })
        )
      );
    }
  }]);

  return Queries;
}(React.Component);

var QueryParameters = function (_React$Component2) {
  _inherits(QueryParameters, _React$Component2);

  function QueryParameters() {
    _classCallCheck(this, QueryParameters);

    return _possibleConstructorReturn(this, (QueryParameters.__proto__ || Object.getPrototypeOf(QueryParameters)).apply(this, arguments));
  }

  _createClass(QueryParameters, [{
    key: "render",
    value: function render() {
      var _this3 = this;

      return React.createElement(
        "div",
        null,
        React.createElement(
          "label",
          { htmlFor: "parameters" },
          "Parameters"
        ),
        React.createElement(
          "div",
          { id: "parameters" },
          this.props.query.parameters.map(function (parameter, index) {
            return React.createElement(
              "div",
              { key: index },
              React.createElement(
                "div",
                { className: "input-group mb-3" },
                React.createElement(
                  "div",
                  { className: "input-group-prepend" },
                  React.createElement(
                    "span",
                    { className: "input-group-text" },
                    parameter.name
                  )
                ),
                React.createElement(
                  "select",
                  { onChange: _this3.props.selectQueryParameter.bind(null, index), className: "custom-select" },
                  React.createElement(
                    "option",
                    { key: "all" },
                    "all"
                  ),
                  parameter.values.map(function (value) {
                    return React.createElement(
                      "option",
                      { key: value.name },
                      value.name
                    );
                  })
                )
              )
            );
          })
        )
      );
    }
  }]);

  return QueryParameters;
}(React.Component);

var QueryFields = function (_React$Component3) {
  _inherits(QueryFields, _React$Component3);

  function QueryFields() {
    _classCallCheck(this, QueryFields);

    return _possibleConstructorReturn(this, (QueryFields.__proto__ || Object.getPrototypeOf(QueryFields)).apply(this, arguments));
  }

  _createClass(QueryFields, [{
    key: "render",
    value: function render() {
      var _this5 = this;

      return React.createElement(
        "div",
        null,
        React.createElement(
          "label",
          { htmlFor: "test" },
          "Fields"
        ),
        React.createElement(
          "div",
          { id: "fields" },
          this.props.query.fields.map(function (field, index) {
            return React.createElement(
              "div",
              { className: "form-check form-check-inline mb-3", key: field.name },
              React.createElement("input", { onChange: _this5.props.selectQueryFields.bind(null, index),
                className: "form-check-input", type: "checkbox", checked: field.selected, id: 'fields' + index }),
              React.createElement(
                "label",
                { className: "form-check-label", htmlFor: 'fields' + index },
                field.name
              )
            );
          })
        )
      );
    }
  }]);

  return QueryFields;
}(React.Component);

var Results = function (_React$Component4) {
  _inherits(Results, _React$Component4);

  function Results() {
    _classCallCheck(this, Results);

    return _possibleConstructorReturn(this, (Results.__proto__ || Object.getPrototypeOf(Results)).apply(this, arguments));
  }

  _createClass(Results, [{
    key: "render",
    value: function render() {
      var fields = this.props.query.fields.filter(function (field) {
        return field.selected;
      });
      return React.createElement(
        "div",
        null,
        React.createElement(
          "h4",
          null,
          "Results"
        ),
        React.createElement(
          "table",
          { className: "table" },
          React.createElement(
            "thead",
            null,
            React.createElement(
              "tr",
              null,
              fields.map(function (field, index) {
                return React.createElement(
                  "th",
                  { key: index, scope: "col" },
                  field.name
                );
              })
            )
          ),
          React.createElement(
            "tbody",
            null,
            this.props.results.map(function (item, index) {
              return React.createElement(
                "tr",
                { key: index },
                fields.map(function (field, index) {
                  return React.createElement(
                    "td",
                    { key: index },
                    item[field.name]
                  );
                })
              );
            })
          )
        )
      );
    }
  }]);

  return Results;
}(React.Component);

var App = function (_React$Component5) {
  _inherits(App, _React$Component5);

  function App(props) {
    _classCallCheck(this, App);

    var _this7 = _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).call(this, props));

    _this7.url = "https://us-central1-sheeking-shelter-8443b.cloudfunctions.net/api/graphql";
    _this7.state = {
      loading: true,
      queries: null,
      selectedQuery: null,
      queryString: null,
      results: null
    };
    return _this7;
  }

  _createClass(App, [{
    key: "componentDidMount",
    value: function componentDidMount() {
      this.fetchApiMetadata();
    }
  }, {
    key: "onSelectQuery",
    value: function onSelectQuery(event) {
      var _this8 = this;

      var selectedQuery = this.state.queries[event.target.selectedIndex - 1];
      var queryString = this.writeQuery(selectedQuery);
      this.setState({
        selectedQuery: selectedQuery,
        queryString: queryString,
        loading: true
      }, function () {
        return _this8.executeQuery();
      });
    }
  }, {
    key: "onSelectQueryParameter",
    value: function onSelectQueryParameter(parameterIndex, event) {
      var _this9 = this;

      var selectedQuery = this.state.selectedQuery;
      var value = selectedQuery.parameters[parameterIndex].values[event.target.selectedIndex - 1].name;
      selectedQuery.parameters[parameterIndex].selectedValue = value;
      var queryString = this.writeQuery(selectedQuery);
      this.setState({
        selectedQuery: selectedQuery,
        queryString: queryString,
        loading: true
      }, function () {
        return _this9.executeQuery();
      });
    }
  }, {
    key: "onSelectQueryFields",
    value: function onSelectQueryFields(index, event) {
      var _this10 = this;

      var activate = event.target.checked;
      var selectedQuery = this.state.selectedQuery;
      selectedQuery.fields[index].selected = activate;
      var queryString = this.writeQuery(selectedQuery);
      this.setState({
        selectedQuery: selectedQuery,
        queryString: queryString,
        loading: activate
      }, function () {
        if (activate) {
          _this10.executeQuery();
        }
      });
    }
  }, {
    key: "fetchApiMetadata",
    value: function fetchApiMetadata() {
      var _this11 = this;

      axios.post(this.url, {
        query: "\n      {\n        __type(name: \"Query\") {\n          name\n          fields {\n            name\n            type {\n              ofType {\n                ofType {\n                  ofType {\n                    name\n                    fields {\n                      name\n                    }\n                  }\n                }\n              }\n            }\n            args {\n              name\n              type {\n                name\n                enumValues {\n                  name\n                }\n              }\n            }\n          }\n        }\n      }\n      "
      }).then(function (response) {
        var queries = response.data.data.__type.fields.map(function (query) {
          return {
            name: query.name,
            parameters: query.args.map(function (arg) {
              return {
                name: arg.name,
                values: arg.type.enumValues.map(function (value) {
                  return {
                    name: value.name
                  };
                })
              };
            }),
            fields: query.type.ofType.ofType.ofType.fields.map(function (field) {
              return {
                name: field.name,
                selected: true
              };
            })
          };
        });
        _this11.setState({
          loading: false,
          queries: queries
        });
      }).catch(function (error) {
        console.log(error);
      });
    }
  }, {
    key: "writeQuery",
    value: function writeQuery(query) {
      var parameters = query.parameters.filter(function (parameter) {
        return parameter.selectedValue;
      });
      var parameterString = parameters.length ? "(" + parameters.map(function (parameter) {
        return parameter.name + ": " + parameter.selectedValue;
      }).join(',') + ")" : '';
      var fieldsString = query.fields.filter(function (field) {
        return field.selected;
      }).map(function (field) {
        return field.name;
      }).join('\n');
      var queryString = "\n    query {\n      " + query.name + parameterString + " {\n        " + fieldsString + "\n      }\n    }\n    ";
      return queryString;
    }
  }, {
    key: "executeQuery",
    value: function executeQuery() {
      var _this12 = this;

      this.setState({
        results: null,
        loading: true
      });
      axios.post(this.url, {
        query: this.state.queryString
      }).then(function (response) {
        _this12.setState({
          loading: false,
          results: response.data.data[_this12.state.selectedQuery.name]
        });
      }).catch(function (error) {
        return console.log(error);
      });
    }
  }, {
    key: "render",
    value: function render() {
      var _state = this.state,
          loading = _state.loading,
          queries = _state.queries,
          selectedQuery = _state.selectedQuery,
          results = _state.results;

      return React.createElement(
        "div",
        null,
        React.createElement(
          "h4",
          null,
          "Query"
        ),
        queries ? React.createElement(Queries, { queries: queries, selectQuery: this.onSelectQuery.bind(this) }) : React.createElement(
          "p",
          null,
          "Loading query metadata..."
        ),
        selectedQuery && React.createElement(
          "div",
          null,
          React.createElement(QueryParameters, { query: selectedQuery, selectQueryParameter: this.onSelectQueryParameter.bind(this) }),
          React.createElement(QueryFields, { query: selectedQuery, selectQueryFields: this.onSelectQueryFields.bind(this) })
        ),
        results && React.createElement(Results, { query: selectedQuery, results: results }),
        loading && React.createElement(
          "div",
          { className: "progress" },
          React.createElement("div", { className: "progress-bar progress-bar-striped progress-bar-animated", role: "progressbar", style: { width: '100%' } })
        )
      );
    }
  }]);

  return App;
}(React.Component);

var domContainer = document.querySelector('#app');
ReactDOM.render(React.createElement(App, null), domContainer);