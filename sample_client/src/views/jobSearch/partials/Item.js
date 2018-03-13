import React, {Component} from 'react';

import {connect} from 'react-redux';
import Icon from "../../../utils/icon";
import logo from '../job-company-logo-01.jpg';
import ReactHtmlParser, {convertNodeToElement} from 'react-html-parser';
import moment from "moment/moment";
import ReadMore from "../../../utils/ReadMore";

class Item extends Component {
    cursorStyles = {
        cursor: 'pointer'
    };

    transform = (node, index) => {
        // Transform <html> and <body> into <div>
        if (node.type === 'tag' && (node.name === 'html' || node.name === 'body')) {
            node.name = 'div';
            return convertNodeToElement(node, index, this.transform);
        }
    };

    options = {
        decodeEntities: true,
        transform: this.transform
    };

    parseHTML = (html) => {
        return ReactHtmlParser(html, this.options)
    };

    render() {
        let end_date = moment().toDate();
        let duration = moment.duration(moment(end_date).diff(this.props.item.modified)).humanize();
        return (
            <div className="job-card bg-white p-3">
                <div className="row">
                    <div className="col-sm-9 col-md-9">
                        <h5 className="float-left">{this.props.item.name}</h5>
                    </div>
                    <div className="col-sm-3 col-md-3">
                        <span className="text-muted float-right">{duration} ago</span>
                    </div>
                </div>
                <div className="row">
                    <div className="col-sm-3 col-md-2">
                        <img className="border img-fluid" src={logo} alt="Logo"/>
                    </div>
                    <div className="col-sm">
                        <div className="row">
                            <div className="col"><p className="mb-0">{this.props.item.company}</p></div>
                        </div>
                        <div className="row">
                            <div className="col-4"><p className="text-muted">{this.props.item.location}</p></div>
                            <div className="col">
                                <p className="text-muted">
                                    {this.props.item.salary_from ? 'from £ ' + this.props.item.salary_from : null}
                                    {this.props.item.salary_to ? 'to £ ' + this.props.item.salary_to : null}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        <div className="text-muted text-justify">
                            <ReadMore lines={6} moreText="Read more" lessText="Less">
                                {this.parseHTML(this.props.item.descr)}
                            </ReadMore>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col">
                        <p className="rating float-left mt-2 mb-0">
                            <Icon name='circle-o' className='text-brand'/>
                            <Icon name='circle-o' className='text-brand'/>
                            <Icon name='circle-o' className='text-brand'/>
                            <Icon name='circle-o' className='text-brand'/>
                            <Icon name='circle-o' className='text-brand'/>
                        </p>
                        <p className="submit float-right mb-0"><button className="btn btn-brand px-4 text-uppercase">Apply</button></p>
                    </div>
                </div>
            </div>
        )
    }
}

function mapStateToProps(state) {
    return {
        userId: state.auth.user.id,
        jobProfileId : state.jobProfile.selectedJobProfile ? state.jobProfile.selectedJobProfile.id : null,
    }
}

Item = connect(mapStateToProps)(Item);

export default Item;
