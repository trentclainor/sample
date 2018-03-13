import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Col, Container, Row} from "reactstrap";
import background from './bg-01.jpg';
import SearchForm from "./forms/searchForm";
import {bindActionCreators} from "redux";
import * as actionCreators from "../../actions/vacancy";


class Search extends Component {

    styles = {
        background: `url(${background}) no-repeat center center`,
        backgroundSize: '100% auto'
    };

    handleSubmit = (values) => {
        this.props.actions.applyFilters(values);
        this.props.history.push('/search/results');
    };

    render() {
        return (
            <div className="search-jobs mb-5" style={this.styles}>
                <Container>
                    <Row className='justify-content-center'>
                        <Col md='10'>
                            <h3 className="text-center text-white font-weight-light">Search Jobs</h3>
                            <SearchForm
                                onSubmit={this.handleSubmit}
                                initialValues={this.props.filters}
                                enableReinitialize={true}/>

                            <p className="text-center text-white">
                                {'Recent Searches:  '}
                                <a className="text-white" href="#">
                                    <small>Business Analyst</small>
                                </a>
                                {', '}
                                <a className="text-white" href="#">
                                    <small>Business Specialist</small>
                                </a>
                                {', '}
                                <a className="text-white" href="#">
                                    <small>Business Executive</small>
                                </a>
                            </p>
                        </Col>
                    </Row>
                </Container>
            </div>

        )
    }
}

function mapStateToProps(state) {

    return {
        vacancies: state.vacancy.items,
        filters: state.vacancy.filters,
        loading: state.vacancy.loading,
        errors: state.vacancy.errors,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

Search = connect(mapStateToProps, mapDispatchToProps)(Search);
export default Search;
