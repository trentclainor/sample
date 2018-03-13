import React, { Component} from 'react';
import { connect } from 'react-redux';

import LanguageItem from './languageItem';


class LanguageList extends Component {

    languageList = () => {
        return this.props.languages.map(language => {
            return (
                <LanguageItem key={language.id} language={language}/>
            )
        })
    };

    render() {
        return (
            <div>
                {this.languageList()}
            </div>
        )
    }
}

function mapStateToProps(state) {

  return {
      languages: state.profileLanguage.languages,
  }
}

export default connect(mapStateToProps)(LanguageList);
