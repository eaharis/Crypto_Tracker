// useCryptoTableLogic.js
import { useState, useEffect } from 'react';
import axios from 'axios';

const ITEMS_PER_PAGE = 50;

/**
 * Returns an object with sorted, paginated cryptos plus handler functions.
 */
export function useCryptoTableLogic() {
    const [cryptos, setCryptos] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);

    // Default sort: rank ascending
    const [sortConfig, setSortConfig] = useState({
        key: 'cmc_rank',
        direction: 'asc',
    });

    useEffect(() => {
        fetchAllCryptos();
    }, []);

    // Fetch data from your backend (returns all cryptos)
    const fetchAllCryptos = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:8000/cryptos/all');
            setCryptos(response.data?.cryptos || []);
        } catch (err) {
            console.error('Failed to fetch cryptos:', err);
        }
    };

    // Sorting
    const getSortedCryptos = () => {
        const sorted = [...cryptos];
        sorted.sort((a, b) => {
            const quoteA = a.quote?.USD || {};
            const quoteB = b.quote?.USD || {};

            let valA, valB;
            switch (sortConfig.key) {
                case 'cmc_rank':
                    valA = a.cmc_rank;
                    valB = b.cmc_rank;
                    break;
                case 'price':
                    valA = quoteA.price || 0;
                    valB = quoteB.price || 0;
                    break;
                case 'volume_24h':
                    valA = quoteA.volume_24h || 0;
                    valB = quoteB.volume_24h || 0;
                    break;
                case 'market_cap':
                    valA = quoteA.market_cap || 0;
                    valB = quoteB.market_cap || 0;
                    break;
                case 'percent_change_24h':
                    valA = quoteA.percent_change_24h || 0;
                    valB = quoteB.percent_change_24h || 0;
                    break;
                default:
                    valA = 0;
                    valB = 0;
            }

            if (valA < valB) {
                return sortConfig.direction === 'asc' ? -1 : 1;
            } else if (valA > valB) {
                return sortConfig.direction === 'asc' ? 1 : -1;
            }
            return 0;
        });
        return sorted;
    };

    // Toggle or set the sort column
    const handleSort = (key) => {
        if (sortConfig.key === key) {
            // Toggle direction
            setSortConfig({
                key,
                direction: sortConfig.direction === 'asc' ? 'desc' : 'asc',
            });
        } else {
            // New column, start with ascending
            setSortConfig({
                key,
                direction: 'asc',
            });
        }
    };

    // Pagination
    const sortedCryptos = getSortedCryptos();
    const totalPages = Math.ceil(sortedCryptos.length / ITEMS_PER_PAGE);
    const startIndex = (currentPage - 1) * ITEMS_PER_PAGE;
    const endIndex = startIndex + ITEMS_PER_PAGE;
    const currentPageData = sortedCryptos.slice(startIndex, endIndex);

    const handlePageChange = (newPage) => {
        if (newPage >= 1 && newPage <= totalPages) {
            setCurrentPage(newPage);
        }
    };

    // Number formatting
    const formatLargeNumber = (num) => {
        if (!num || num <= 0) return '—';
        if (num >= 1e9) return (num / 1e9).toFixed(2) + ' B';
        if (num >= 1e6) return (num / 1e6).toFixed(2) + ' M';
        return num.toFixed(2);
    };

    return {
        sortConfig,
        handleSort,
        currentPage,
        handlePageChange,
        totalPages,
        currentPageData,
        formatLargeNumber,
    };
}