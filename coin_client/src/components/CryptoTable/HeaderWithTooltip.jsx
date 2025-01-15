// HeaderWithTooltip.jsx
import React from 'react';
import Tooltip from '@mui/material/Tooltip';

/**
 * Displays a column title, plus a “?” tooltip icon, plus an optional sort arrow.
 */
const HeaderWithTooltip = ({
                               title,
                               tooltip,
                               sortable = false,
                               sortActive = false,
                               sortDirection = 'asc'
                           }) => {
    return (
        <span className="headerClickable">
      {title}
            {tooltip && (
                <Tooltip title={tooltip} arrow>
                    <span className="questionIcon">?</span>
                </Tooltip>
            )}
            {sortable && sortActive && (
                <span className="sortIndicator">
          {sortDirection === 'asc' ? '▲' : '▼'}
        </span>
            )}
    </span>
    );
};

export default HeaderWithTooltip;