import React, { Component} from 'react';
import { connect } from 'react-redux';

import WorkHistoryItem from './workHistoryItem';


class WorkHistoryList extends Component {

    workHistoryList = () => {
        return this.props.workHistories.map(workHistory => {
            return (
                <WorkHistoryItem key={workHistory.id} workHistory={workHistory}/>
            )
        })
    };

    render() {
        return (
            <div>
                {this.workHistoryList()}
            </div>
        )
    }
}

function mapStateToProps(state) {

    return {
        workHistories: state.profileWorkHistory.workHistories,
    }
}

export default connect(mapStateToProps)(WorkHistoryList);
