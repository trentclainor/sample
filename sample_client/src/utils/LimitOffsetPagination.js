import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {Pagination, PaginationItem, PaginationLink} from "reactstrap";
import {COUNT_PER_PAGE} from "./config";
import {range} from "./index";


class LimitOffsetPagination extends Component {

    getDisplayedPageNumbers(current, final){
        /*
            This utility function determines a list of page numbers to display.
            This gives us a nice contextually relevant set of page numbers.
            For example:
            current=14, final=16 -> [1, None, 13, 14, 15, 16]
            This implementation gives one page to each side of the cursor,
            or two pages to the side when the cursor is at the edge, then
            ensures that any breaks between non-continuous page numbers never
            remove only a single page.
            For an alternative implementation which gives two pages to each side of
            the cursor, eg. as in GitHub issue list pagination, see:
            https://gist.github.com/tomchristie/321140cebb1c4a558b15
        */
        if (final <= 5){
            return range(1, final)
        }

        // We always include the first two pages, last two pages, and
        // two pages either side of the current page.
        let included = new Set();
        included.add(1);
        included.add(current - 1);
        included.add(current);
        included.add(current + 1);
        included.add(final);

        // If the break would only exclude a single page number then we
        // may as well include the page number instead of the break.
        if (current <= 4){
            included.add(2);
            included.add(3);
        }

        if (current >= final - 3){
            included.add(final - 1);
            included.add(final - 2) ;
        }

        let insideConditions = (value) => {
            return value <= final && value > 0;
        };

        included = [...included];

        // Now sort the page numbers and drop anything outside the limits.
        included.sort(function(a, b) {
            return a - b;
        });
        included = included.filter(insideConditions);

        //Finally insert any `...` breaks
        if (current > 4){
            included.splice(1, 0, '...')
        }

        if (current < final - 3) {
            included.splice(included.length - 1, 0, '...')
        }
        return included
    }

    changePage(page){
        this.props.onChange({
            limit: this.props.countPerPage,
            offset: this.props.countPerPage * (page - 1)
        });
    }

    getPrevPaginationItem(currentPage){
        return (
            <PaginationItem disabled={currentPage === 1}>
                <PaginationLink previous
                                onClick={() => this.changePage(currentPage - 1)}/>
            </PaginationItem>
        )
    }

    getNextPaginationItem(currentPage, countOfPages){
        return (
            <PaginationItem disabled={currentPage === countOfPages}>
                <PaginationLink next
                                onClick={() => this.changePage(currentPage + 1)}/>
            </PaginationItem>
        )
    }

    getPaginationNumberItems(currentPage, displayedPages){
        return (
            displayedPages.map((item, index) => {
                return (
                    item === '...' ?
                        <PaginationItem key={index} disabled>
                            <PaginationLink>
                                {item}
                            </PaginationLink>
                        </PaginationItem>
                        :
                        <PaginationItem key={index} active={item === currentPage}>
                            <PaginationLink onClick={() => { if(currentPage !== item){this.changePage(item)}}}>
                                {item}
                            </PaginationLink>
                        </PaginationItem>
                )
            })
        )
    }

    render() {
        if (this.props.total < this.props.countPerPage){
            return null;
        }

        let positionClass = 'pull-' + this.props.position;
        let countOfPages = (this.props.total - (this.props.total % this.props.countPerPage))/ this.props.countPerPage;

        if (this.props.total % this.props.countPerPage > 0) {
            countOfPages = countOfPages + 1;
        }

        let currentPage = this.props.offset / this.props.countPerPage + 1;

        let displayedPages = this.getDisplayedPageNumbers(currentPage, countOfPages);

        return (
            <Pagination className={positionClass}>
                {this.getPrevPaginationItem(currentPage)}
                {this.getPaginationNumberItems(currentPage, displayedPages)}
                {this.getNextPaginationItem(currentPage, countOfPages)}
            </Pagination>
        )
    }
}

LimitOffsetPagination.defaultProps = {
    position: 'right',
    countPerPage: COUNT_PER_PAGE,
    options: {}
};

LimitOffsetPagination.propTypes = {
    position: PropTypes.node,
    limit: PropTypes.number,
    offset: PropTypes.number,
    total: PropTypes.number,
    countPerPage: PropTypes.number,
    options: PropTypes.object,
};

export default LimitOffsetPagination;
