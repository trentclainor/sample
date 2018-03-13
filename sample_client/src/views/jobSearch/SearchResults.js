import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Col, Container, Row} from "reactstrap";
import {bindActionCreators} from "redux";
import * as actionCreators from "../../actions/vacancy";
import SearchForm from "./forms/searchResultsForm";
import {filterObjectByKey, isEmpty} from "../../utils";
import FilterPanel from "./forms/filterPanelForm";
import List from "./partials/List";


class SearchResults extends Component {

    componentDidMount() {
        if (this.props.filters.search_type === 'Standard') {
            let filters = filterObjectByKey(
                this.props.filters,
                ['search_type', 'job_profile_id', 'limit', 'offset', 'ordering']
            );

            if (!isEmpty(filters)) {
                this.props.actions.standardSearch(filters);
            }
        }
        if (this.props.filters.search_type === 'Personalised'){
            let filters = filterObjectByKey(
                this.props.filters,
                ['search_type', 'name', 'location', 'limit', 'offset', 'ordering']
            );

            if (!isEmpty(filters)) {
                this.props.actions.personalizedSearch(filters);
            }
        }
    }

    componentWillReceiveProps(nextProps) {
        if (this.props.filters !== nextProps.filters){
            if (nextProps.filters.search_type === 'Standard') {
                let filters = filterObjectByKey(nextProps.filters, ['search_type', 'job_profile_id']);
                if (!isEmpty(filters)) {
                    nextProps.actions.standardSearch(filters);
                }
            }
            if (nextProps.filters.search_type === 'Personalised'){
                let filters = filterObjectByKey(nextProps.filters, ['search_type', 'name', 'location']);
                if (!isEmpty(filters)) {
                    nextProps.actions.personalizedSearch(filters);
                }
            }
        }
    }

    handleSubmit = (values) => {
        // enable first page for new search
        values['offset'] = 0;

        this.props.actions.applyFilters(values);
    };

    render() {
        return (
            <Container className='mb-3'>
                <Row className='search-jobs-small justify-content-center my-3'>
                    <Col xl='7'>
                        <SearchForm
                            onSubmit={this.handleSubmit}
                            initialValues={this.props.filters}
                            enableReinitialize={true}/>
                    </Col>
                </Row>
                <Row>

                    <Col xl='8' md='8' sm='12' xs='12'>
                        <List/>
                    </Col>
                    <Col xl='4' md='4' sm='12' xs='12' className='order-md-first'>
                        <FilterPanel
                            onSubmit={this.handleSubmit}
                        />
                    </Col>
                </Row>
            </Container>
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

SearchResults = connect(mapStateToProps, mapDispatchToProps)(SearchResults);
export default SearchResults;
