import React, {Component} from 'react';
import {connect} from 'react-redux';

import Item from './Item';
import {Alert, Col, Input, Row} from "reactstrap";
import LimitOffsetPagination from "../../../utils/LimitOffsetPagination";
import * as actionCreators from "../../../actions/vacancy";
import {bindActionCreators} from "redux";
import Loader from "../../../utils/Loader";


class List extends Component {

    List = () => {
        return this.props.items.map(item => {
            return (
                <Item key={item.id} item={item}/>
            )
        })
    };

    orderByField = [
        {value: "modified", title: "Posted date (asc)"},
        {value: "-modified", title: "Posted date (desc)"},
        {value: "name", title: "Name (asc)"},
        {value: "-name", title: "Name (desc)"},
    ];

    changeOrdering = (event) => {
        this.props.actions.applyFilters({ordering: event.target.value})
    };

    render() {
        return (
            <div>
                {
                    !this.props.itemsCount ?
                        <Loader loading={this.props.loading}>
                            <Row>
                                <Col>
                                    <div className="job-card bg-white p-3">
                                        <Alert color="info">
                                            <h4>Nothing Found</h4>
                                            Sorry, but nothing matched your search terms. Please try again with some different keywords.
                                        </Alert>
                                    </div>
                                </Col>
                            </Row>
                        </Loader>
                        :
                        <div>
                            <Row>
                                <Col md='auto' className='mr-auto'>
                                    <h4>
                                        {this.props.itemsCount} Jobs
                                        {
                                            this.props.filters.search_type === 'Standard' ?
                                                this.props.filters.name ?
                                                    " for '" + this.props.filters.name + "'"
                                                    : null
                                                : " for selected CV"
                                        }
                                        <small className="d-block text-muted">London, UK</small>
                                    </h4>
                                </Col>
                                <Col lg='5' className='form-inline d-flex justify-content-md-end'>
                                    <label htmlFor="sortOrder" className="mr-2">Sort By:</label>

                                    <Input
                                        type='select'
                                        className='form-control'
                                        onChange={this.changeOrdering}
                                        defaultValue={this.props.filters.ordering}
                                    >
                                        {this.orderByField.map(item => (
                                            <option value={item.value} key={item.value}>
                                                {item.title}
                                            </option>
                                        ))}
                                    </Input>
                                </Col>
                            </Row>

                            <Row>
                                <Col>
                                    <Loader loading={this.props.loading}>
                                        {this.List()}
                                    </Loader>

                                </Col>
                            </Row>
                            <Row>
                                <Col className='mt-3'>
                                    <LimitOffsetPagination
                                        total={this.props.itemsCount}
                                        limit={this.props.filters.limit}
                                        offset={this.props.filters.offset}
                                        onChange={this.props.actions.applyFilters}
                                    />
                                </Col>
                            </Row>
                        </div>
                }
            </div>

        )
    }
}

function mapStateToProps(state) {

    return {
        loading: state.vacancy.loading,
        items: state.vacancy.items,
        itemsCount: state.vacancy.itemsCount,
        filters: state.vacancy.filters,
    }
}

const mapDispatchToProps = (dispatch) => {
    return {
        dispatch,
        actions: bindActionCreators(actionCreators, dispatch)
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(List);
