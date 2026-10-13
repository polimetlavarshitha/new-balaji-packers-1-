/**
 * New Balaji Packers and Movers - Interactive Price Calculator
 * Feature 1: Real-time dynamic quotation estimation tool
 */

(function () {
    'use strict';

    // Approximate road distance matrix between key locations (in km)
    const DISTANCE_MATRIX = {
        'Vuyyuru-Vijayawada': 32,
        'Vijayawada-Vuyyuru': 32,
        'Vuyyuru-Machilipatnam': 48,
        'Machilipatnam-Vuyyuru': 48,
        'Vijayawada-Machilipatnam': 70,
        'Machilipatnam-Vijayawada': 70,
        'Vuyyuru-Guntur': 55,
        'Vijayawada-Guntur': 35,
        'Machilipatnam-Guntur': 95,
        'Vuyyuru-Hyderabad': 295,
        'Vijayawada-Hyderabad': 275,
        'Machilipatnam-Hyderabad': 345,
        'Vuyyuru-Bangalore': 640,
        'Vijayawada-Bangalore': 630,
        'Machilipatnam-Bangalore': 690,
        'Vuyyuru-Chennai': 440,
        'Vijayawada-Chennai': 430,
        'Machilipatnam-Chennai': 410,
        'Vuyyuru-Visakhapatnam': 370,
        'Vijayawada-Visakhapatnam': 350,
        'Machilipatnam-Visakhapatnam': 400,
    };

    // Base pricing according to relocation type
    const MOVE_TYPE_PRICING = {
        '1bhk': { base: 3500, label: '1 BHK / Small Shifting', ratePerKm: 28 },
        '2bhk': { base: 5500, label: '2 BHK Shifting', ratePerKm: 34 },
        '3bhk': { base: 8200, label: '3 BHK Shifting', ratePerKm: 42 },
        'villa': { base: 12500, label: '4 BHK / Villa Shifting', ratePerKm: 52 },
        'office': { base: 7000, label: 'Office & IT Relocation', ratePerKm: 40 },
        'vehicle': { base: 4000, label: 'Vehicle Transportation Only', ratePerKm: 22 },
        'local': { base: 2800, label: 'Local Room / Few Items', ratePerKm: 25 },
    };

    // Item unit pricing for calculator
    const ITEM_VALUES = {
        'bed': { name: 'Double Bed & Mattress', price: 650 },
        'sofa': { name: 'Sofa Set', price: 700 },
        'fridge': { name: 'Refrigerator', price: 450 },
        'washing': { name: 'Washing Machine', price: 400 },
        'tv': { name: 'Smart TV & Unit', price: 350 },
        'dining': { name: 'Dining Table & Chairs', price: 500 },
        'almirah': { name: 'Wardrobe / Cupboard', price: 600 },
        'ac': { name: 'Split AC Unit', price: 550 },
        'boxes': { name: 'Carton Boxes (5+)', price: 400 },
        'bike': { name: 'Two-Wheeler / Bike', price: 1200 },
    };

    function initCalculator() {
        const pickupSelect = document.getElementById('calc-pickup');
        const dropSelect = document.getElementById('calc-drop');
        const moveTypeSelect = document.getElementById('calc-move-type');
        const packingTierSelect = document.getElementById('calc-packing-tier');
        const floorSelect = document.getElementById('calc-floor');
        const itemCheckboxes = document.querySelectorAll('.calc-item-checkbox');

        const totalReadout = document.getElementById('calc-total-price');
        const distanceReadout = document.getElementById('calc-distance');
        const transportCostReadout = document.getElementById('calc-transport-cost');
        const packingCostReadout = document.getElementById('calc-packing-cost');
        const laborCostReadout = document.getElementById('calc-labor-cost');
        const bookEstimateBtn = document.getElementById('calc-book-btn');

        if (!pickupSelect || !dropSelect || !totalReadout) return;

        function calculate() {
            const pickup = pickupSelect.value;
            const drop = dropSelect.value;
            const moveTypeKey = moveTypeSelect.value || '2bhk';
            const tier = packingTierSelect ? packingTierSelect.value : 'premium';
            const floorOption = floorSelect ? floorSelect.value : 'ground';

            // Determine estimated distance
            let distance = 25; // default local distance
            if (pickup && drop) {
                if (pickup === drop) {
                    distance = 12; // local within city
                } else {
                    const key1 = `${pickup}-${drop}`;
                    const key2 = `${drop}-${pickup}`;
                    if (DISTANCE_MATRIX[key1]) {
                        distance = DISTANCE_MATRIX[key1];
                    } else if (DISTANCE_MATRIX[key2]) {
                        distance = DISTANCE_MATRIX[key2];
                    } else {
                        distance = 150; // generic regional distance
                    }
                }
            }

            const moveConfig = MOVE_TYPE_PRICING[moveTypeKey] || MOVE_TYPE_PRICING['2bhk'];
            
            // Transport Calculation
            let transportFee = moveConfig.base + Math.round(distance * moveConfig.ratePerKm);

            // Item Add-ons
            let itemsAddon = 0;
            const selectedItemNames = [];
            itemCheckboxes.forEach(cb => {
                if (cb.checked) {
                    const val = cb.value;
                    if (ITEM_VALUES[val]) {
                        itemsAddon += ITEM_VALUES[val].price;
                        selectedItemNames.push(ITEM_VALUES[val].name);
                    }
                }
            });

            // Packing Material Tier Factor
            let packingMultiplier = 1.0;
            let packingBase = 1200 + Math.round(itemsAddon * 0.4);
            if (tier === 'premium') {
                packingMultiplier = 1.25;
            } else if (tier === 'wooden_crate') {
                packingMultiplier = 1.5;
            }
            let packingFee = Math.round(packingBase * packingMultiplier);

            // Loading, Unloading & Floor Surcharge
            let laborFee = 1500;
            if (floorOption === 'stairs_high') {
                laborFee += 1200; // 3rd floor or higher without elevator
            } else if (floorOption === 'stairs_low') {
                laborFee += 500;  // 1st or 2nd floor without elevator
            }

            // Total
            let totalEstimated = transportFee + packingFee + laborFee + itemsAddon;

            // Round to nearest 50 for realistic quote
            totalEstimated = Math.ceil(totalEstimated / 50) * 50;

            // Update UI Readouts with smooth transition
            if (totalReadout) {
                totalReadout.textContent = `₹${totalEstimated.toLocaleString('en-IN')}`;
            }
            if (distanceReadout) {
                distanceReadout.textContent = `${distance} km approx`;
            }
            if (transportCostReadout) {
                transportCostReadout.textContent = `₹${transportFee.toLocaleString('en-IN')}`;
            }
            if (packingCostReadout) {
                packingCostReadout.textContent = `₹${packingFee.toLocaleString('en-IN')}`;
            }
            if (laborCostReadout) {
                laborCostReadout.textContent = `₹${(laborFee + itemsAddon).toLocaleString('en-IN')}`;
            }

            // Update "Book with this Estimate" link parameters
            if (bookEstimateBtn) {
                const params = new URLSearchParams({
                    pickup: pickup || 'Vuyyuru',
                    drop: drop || 'Vijayawada',
                    move_type: moveTypeKey === 'vehicle' ? 'car' : (moveTypeKey === 'office' ? 'office' : 'household'),
                    price: totalEstimated,
                    tier: tier,
                    items: selectedItemNames.join(', ')
                });
                bookEstimateBtn.href = `/quote/?${params.toString()}`;
            }
        }

        // Attach event listeners
        pickupSelect.addEventListener('change', calculate);
        dropSelect.addEventListener('change', calculate);
        moveTypeSelect.addEventListener('change', calculate);
        if (packingTierSelect) packingTierSelect.addEventListener('change', calculate);
        if (floorSelect) floorSelect.addEventListener('change', calculate);
        itemCheckboxes.forEach(cb => cb.addEventListener('change', calculate));

        // Initial run
        calculate();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCalculator);
    } else {
        initCalculator();
    }
})();
