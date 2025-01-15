// CryptoTable.jsx
import React from 'react';
import {
    Table, TableHead, TableBody, TableRow, TableCell,
    Paper, TableContainer, Box
} from '@mui/material';
import HeaderWithTooltip from './HeaderWithTooltip';
import { useCryptoTableLogic } from './useCryptoTableLogic';
import './CryptoTable.css'; // Import the separate CSS file

function CryptoTable() {
    const {
        sortConfig,
        handleSort,
        currentPage,
        handlePageChange,
        totalPages,
        currentPageData,
        formatLargeNumber
    } = useCryptoTableLogic();

    // Render pagination row
    const renderPagination = () => {
        const pages = [];
        pages.push(1);
        let startRange = Math.max(currentPage - 2, 2);
        let endRange = Math.min(currentPage + 2, totalPages - 1);

        if (startRange < 2) startRange = 2;
        if (endRange > totalPages - 1) endRange = totalPages - 1;

        for (let i = startRange; i <= endRange; i++) {
            pages.push(i);
        }
        if (totalPages > 1) pages.push(totalPages);

        return (
            <div className="paginationContainer">
        <span
            className={`pageLink ${currentPage <= 1 ? 'disabledLink' : ''}`}
            onClick={() => handlePageChange(currentPage - 1)}
        >
          &lt;
        </span>

                {pages.map((p, idx) => {
                    if (idx > 0 && p - pages[idx - 1] > 1) {
                        // Insert an ellipsis
                        return (
                            <React.Fragment key={`gap-${p}`}>
                                <span className="ellipsis">...</span>
                                <span
                                    className={`pageLink ${p === currentPage ? 'activeLink' : ''}`}
                                    onClick={() => handlePageChange(p)}
                                >
                  {p}
                </span>
                            </React.Fragment>
                        );
                    }
                    return (
                        <span
                            key={p}
                            className={`pageLink ${p === currentPage ? 'activeLink' : ''}`}
                            onClick={() => handlePageChange(p)}
                        >
              {p}
            </span>
                    );
                })}

                <span
                    className={`pageLink ${currentPage >= totalPages ? 'disabledLink' : ''}`}
                    onClick={() => handlePageChange(currentPage + 1)}
                >
          &gt;
        </span>
            </div>
        );
    };

    return (
        <Box sx={{ p: 2 }}>
            <TableContainer component={Paper}>
                <Table>
                    <TableHead>
                        <TableRow sx={{ backgroundColor: '#f9f9f9' }}>
                            <TableCell onClick={() => handleSort('cmc_rank')}>
                                <HeaderWithTooltip
                                    title="#"
                                    tooltip="Rank is the position of a cryptocurrency by Market Cap."
                                    sortable
                                    sortActive={sortConfig.key === 'cmc_rank'}
                                    sortDirection={sortConfig.direction}
                                />
                            </TableCell>
                            <TableCell>
                                {/* Name is not sortable. No tooltip. */}
                                Name
                            </TableCell>
                            <TableCell onClick={() => handleSort('price')}>
                                <HeaderWithTooltip
                                    title="Price"
                                    tooltip="Price is the cost of a single coin or token for a cryptocurrency. It is influenced by supply & demand, availibility, and many other factors."
                                    sortable
                                    sortActive={sortConfig.key === 'price'}
                                    sortDirection={sortConfig.direction}
                                />
                            </TableCell>
                            <TableCell onClick={() => handleSort('percent_change_24h')}>
                                <HeaderWithTooltip
                                    title="24H Change"
                                    tooltip="24H Change shows the % price difference between now and 24 hours ago."
                                    sortable
                                    sortActive={sortConfig.key === 'percent_change_24h'}
                                    sortDirection={sortConfig.direction}
                                />
                            </TableCell>
                            <TableCell onClick={() => handleSort('volume_24h')}>
                                <HeaderWithTooltip
                                    title="24H Volume"
                                    tooltip="24H Volume shows the number of tokens traded in the market between now and 24 hours ago."
                                    sortable
                                    sortActive={sortConfig.key === 'volume_24h'}
                                    sortDirection={sortConfig.direction}
                                />
                            </TableCell>
                            <TableCell onClick={() => handleSort('market_cap')}>
                                <HeaderWithTooltip
                                    title="Market Cap"
                                    tooltip="Market Cap is a cryptocurrency's total value and is calculated by multiplying the price and circulating supply."
                                    sortable
                                    sortActive={sortConfig.key === 'market_cap'}
                                    sortDirection={sortConfig.direction}
                                />
                            </TableCell>
                        </TableRow>
                    </TableHead>

                    <TableBody>
                        {currentPageData.map((coin) => {
                            const quote = coin.quote?.USD || {};
                            const price = quote.price;
                            const change24h = quote.percent_change_24h;
                            const volume = quote.volume_24h;
                            const marketCap = quote.market_cap;

                            const isNegative = (change24h ?? 0) < 0;

                            return (
                                <TableRow key={coin.id}>
                                    <TableCell>{coin.cmc_rank}</TableCell>
                                    <TableCell>{coin.name}</TableCell>
                                    <TableCell>
                                        {price
                                            ? price >= 1
                                                ? `$${price.toFixed(2)}`
                                                : `$${price.toFixed(Math.min(8, String(price).split('.')[1]?.length || 8))}`
                                            : '—'}
                                    </TableCell>
                                    <TableCell style={{ color: isNegative ? 'red' : 'green' }}>
                                        {change24h ? `${change24h.toFixed(2)}%` : '—'}
                                    </TableCell>
                                    <TableCell>
                                        {volume ? `$${formatLargeNumber(volume)}` : '—'}
                                    </TableCell>
                                    <TableCell>
                                        {marketCap ? `$${formatLargeNumber(marketCap)}` : '—'}
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </TableContainer>

            {renderPagination()}
        </Box>
    );
}

export default CryptoTable;