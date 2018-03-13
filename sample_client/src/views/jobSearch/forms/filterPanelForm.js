import React, {Component} from 'react';
import {connect} from 'react-redux';
import {Button, Col, Form, InputGroup, InputGroupAddon, InputGroupText, Row} from "reactstrap";
import {bindActionCreators} from "redux";
import Icon from "../../../utils/icon";
import CollapsibleCard from "../../../utils/collapsibleCard";
import * as vacancyActions from "../../../actions/vacancy";
import * as dictHelpersActions from "../../../actions/dictHelpers";
import {Field, reduxForm} from "redux-form";
import renderMultipleCheckboxField from "../../../utils/renderMultipleCheckboxField";
import renderMultiselect from "../../../utils/renderMultipleSelectField";


class FilterPanel extends Component {

    componentDidMount() {
        this.props.dictHelpersActions.countryList();
        this.props.dictHelpersActions.stateList();
        this.props.dictHelpersActions.cityList();
        this.props.dictHelpersActions.industryList();
        this.props.dictHelpersActions.roleList();
        this.props.dictHelpersActions.lookingForList();
    }

    render() {
        return (
            <Form>
                <div className="filter-panel bg-white p-3">
                    <h5 className="text-secondary text-uppercase">Filter by:</h5>
                    <CollapsibleCard title='Country'>
                         <Field
                            name='country_id'
                            data={this.props.countryList}
                            valueField='value'
                            textField='title'
                            component={renderMultiselect}
                        />
                    </CollapsibleCard>

                    <CollapsibleCard title='State'>
                        <Field
                            name='state_id'
                            data={this.props.stateList}
                            valueField='value'
                            textField='title'
                            component={renderMultiselect}
                        />
                    </CollapsibleCard>

                    <CollapsibleCard title='City'>
                        <Field
                            name='city_id'
                            data={this.props.cityList}
                            valueField='value'
                            textField='title'
                            component={renderMultiselect}
                        />
                    </CollapsibleCard>

                    <CollapsibleCard title='Industry'>
                        <Field
                            name='industry_id'
                            data={this.props.industryList}
                            valueField='value'
                            textField='title'
                            component={renderMultiselect}
                        />
                    </CollapsibleCard>

                    <CollapsibleCard title='Role'>
                        <Field
                            name='role_id'
                            data={this.props.roleList}
                            valueField='value'
                            textField='title'
                            component={renderMultiselect}
                        />
                    </CollapsibleCard>

                    <CollapsibleCard title='Job Type'>
                        <Field
                            name='types'
                            data={this.props.lookingForList}
                            valueField='value'
                            textField='title'
                            component={renderMultipleCheckboxField}
                        />
                    </CollapsibleCard>

                    {/*<CollapsibleCard title='Skill Match'>*/}
                        {/*<ul className="list-unstyled">*/}
                            {/*<li>*/}
                                {/*<div className="custom-control custom-checkbox">*/}
                                    {/*<input type="checkbox" className="custom-control-input" id="skill5"/>*/}
                                    {/*<label className="custom-control-label" htmlFor="skill5">*/}
                                    {/*<span className="text-brand">*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                    {/*</span>*/}
                                    {/*</label>*/}
                                {/*</div>*/}
                            {/*</li>*/}
                            {/*<li>*/}
                                {/*<div className="custom-control custom-checkbox">*/}
                                    {/*<input type="checkbox" className="custom-control-input" id="skill4"/>*/}
                                    {/*<label className="custom-control-label" htmlFor="skill4">*/}
                                    {/*<span className="text-brand">*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                    {/*</span>*/}
                                    {/*</label>*/}
                                {/*</div>*/}
                            {/*</li>*/}
                            {/*<li>*/}
                                {/*<div className="custom-control custom-checkbox">*/}
                                    {/*<input type="checkbox" className="custom-control-input" id="skill3"/>*/}
                                    {/*<label className="custom-control-label" htmlFor="skill3">*/}
                                    {/*<span className="text-brand">*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                    {/*</span>*/}
                                    {/*</label>*/}
                                {/*</div>*/}
                            {/*</li>*/}
                            {/*<li>*/}
                                {/*<div className="custom-control custom-checkbox">*/}
                                    {/*<input type="checkbox" className="custom-control-input" id="skill2"/>*/}
                                    {/*<label className="custom-control-label" htmlFor="skill2">*/}
                                    {/*<span className="text-brand">*/}
                                        {/*<Icon name='circle-o'/>*/}
                                        {/*<Icon name='circle-o'/>*/}
                                    {/*</span>*/}
                                    {/*</label>*/}
                                {/*</div>*/}
                            {/*</li>*/}
                            {/*<li>*/}
                                {/*<div className="custom-control custom-checkbox">*/}
                                    {/*<input type="checkbox" className="custom-control-input" id="skill1"/>*/}
                                    {/*<label className="custom-control-label" htmlFor="skill1">*/}
                                    {/*<span className="text-brand">*/}
                                        {/*<Icon name='circle-o'/>*/}
                                    {/*</span>*/}
                                    {/*</label>*/}
                                {/*</div>*/}
                            {/*</li>*/}
                        {/*</ul>*/}
                    {/*</CollapsibleCard>*/}
                    <Row className='mt-3'>
                        <Col>
                            <Button className='pull-right' color='brand' onClick={this.props.submit}>Apply filters</Button>
                        </Col>
                    </Row>
                </div>

            </Form>
        )
    }
}

const mapStateToProps = (state) => ({
    filters: state.vacancy.filters,
    countryList: state.dictHelpers.countryList,
    stateList: state.dictHelpers.stateList,
    cityList: state.dictHelpers.cityList,
    industryList: state.dictHelpers.industryList,
    roleList: state.dictHelpers.roleList,
    lookingForList: state.dictHelpers.lookingForList
});

const mapDispatchToProps = (dispatch)  => ({
    dispatch,
    vacancyActions: bindActionCreators(vacancyActions, dispatch),
    dictHelpersActions: bindActionCreators(dictHelpersActions, dispatch),
});

FilterPanel = connect(
    mapStateToProps,
    mapDispatchToProps
)(FilterPanel);


FilterPanel = reduxForm({
    form: 'FilterPanelForm', // a unique identifier for this form
})(FilterPanel);

export default FilterPanel
