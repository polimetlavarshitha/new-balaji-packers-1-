/**
 * New Balaji Packers and Movers - Live Review Star Rating Selector
 * Feature 2: Interactive star rating widget and live AJAX feedback submission
 */

(function () {
    'use strict';

    const SENTIMENT_LABELS = {
        1: "⭐ 1 Star - Needs Improvement",
        2: "⭐⭐ 2 Stars - Fair Service",
        3: "⭐⭐⭐ 3 Stars - Good & Safe",
        4: "⭐⭐⭐⭐ 4 Stars - Very Good & Punctual",
        5: "⭐⭐⭐⭐⭐ 5 Stars - Outstanding! Highly Recommended!"
    };

    function initReviewWidget() {
        const starContainer = document.getElementById('live-star-selector');
        const ratingInput = document.getElementById('id_rating_input') || document.querySelector('input[name="rating"]');
        const sentimentDisplay = document.getElementById('rating-sentiment-text');
        const reviewForm = document.getElementById('customer-review-form');
        const reviewsFeed = document.getElementById('reviews-live-feed');
        const alertBox = document.getElementById('review-alert-box');

        if (!starContainer || !ratingInput) return;

        let currentRating = parseInt(ratingInput.value, 10) || 5;

        // Render interactive stars (5 stars)
        starContainer.innerHTML = '';
        for (let i = 1; i <= 5; i++) {
            const star = document.createElement('span');
            star.classList.add('star-item');
            star.dataset.value = i;
            star.innerHTML = '★';
            star.style.fontSize = '2.2rem';
            star.style.cursor = 'pointer';
            star.style.marginRight = '0.3rem';
            star.style.transition = 'color 0.15s ease, transform 0.15s ease';
            starContainer.appendChild(star);
        }

        const stars = starContainer.querySelectorAll('.star-item');

        function updateStarsVisual(ratingVal, isHover = false) {
            stars.forEach((star, idx) => {
                const val = idx + 1;
                if (val <= ratingVal) {
                    star.style.color = '#f59e0b'; // Amber Gold
                    if (isHover) {
                        star.style.transform = 'scale(1.15)';
                        star.style.textShadow = '0 0 10px rgba(245, 158, 11, 0.6)';
                    } else {
                        star.style.transform = 'scale(1.0)';
                        star.style.textShadow = '0 0 4px rgba(245, 158, 11, 0.3)';
                    }
                } else {
                    star.style.color = '#cbd5e1'; // Inactive slate grey
                    star.style.transform = 'scale(1.0)';
                    star.style.textShadow = 'none';
                }
            });

            if (sentimentDisplay && SENTIMENT_LABELS[ratingVal]) {
                sentimentDisplay.textContent = SENTIMENT_LABELS[ratingVal];
            }
        }

        // Attach hover & click events
        stars.forEach(star => {
            star.addEventListener('mouseenter', function () {
                const hoverVal = parseInt(this.dataset.value, 10);
                updateStarsVisual(hoverVal, true);
            });

            star.addEventListener('click', function () {
                currentRating = parseInt(this.dataset.value, 10);
                ratingInput.value = currentRating;
                updateStarsVisual(currentRating, false);
            });
        });

        starContainer.addEventListener('mouseleave', function () {
            updateStarsVisual(currentRating, false);
        });

        // Initialize display
        updateStarsVisual(currentRating, false);

        // Handle AJAX Review Form Submission
        if (reviewForm) {
            reviewForm.addEventListener('submit', function (e) {
                e.preventDefault();

                const submitBtn = reviewForm.querySelector('button[type="submit"]');
                const originalBtnText = submitBtn ? submitBtn.innerHTML : 'Submit Review';
                if (submitBtn) {
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Posting Review...';
                }

                const formData = new FormData(reviewForm);
                formData.append('is_ajax', '1');

                // Get CSRF Token
                const csrfTokenEl = reviewForm.querySelector('input[name="csrfmiddlewaretoken"]');
                const csrfToken = csrfTokenEl ? csrfTokenEl.value : '';

                fetch(reviewForm.action || '/submit-review/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': csrfToken,
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                    body: formData
                })
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Review submission failed');
                        }
                        return response.json();
                    })
                    .then(data => {
                        if (data.status === 'success') {
                            // Show success message
                            if (alertBox) {
                                alertBox.innerHTML = `
                                    <div class="alert alert-success alert-dismissible fade show shadow-sm" role="alert">
                                        <strong><i class="bi bi-check-circle-fill me-1"></i> Success!</strong> ${data.message}
                                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                    </div>
                                `;
                            }

                            // Dynamically inject the new review into the live feed
                            if (reviewsFeed && data.review) {
                                const newReviewCard = document.createElement('div');
                                newReviewCard.className = 'col-md-6 mb-3';
                                
                                let starIcons = '';
                                for (let s = 1; s <= 5; s++) {
                                    starIcons += s <= data.review.rating 
                                        ? '<i class="bi bi-star-fill text-warning me-1"></i>' 
                                        : '<i class="bi bi-star text-muted me-1"></i>';
                                }

                                newReviewCard.innerHTML = `
                                    <div class="card card-premium h-100 p-4 border-warning shadow-sm animate__animated animate__fadeInDown">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <div>${starIcons}</div>
                                            <span class="badge bg-amber-50 text-amber-700 border border-warning text-dark px-2 py-1 small">
                                                Verified Just Now
                                            </span>
                                        </div>
                                        <p class="fst-italic text-secondary mb-3">"${escapeHtml(data.review.review_text)}"</p>
                                        <div class="d-flex justify-content-between align-items-center pt-2 border-top">
                                            <span class="fw-bold text-dark">— ${escapeHtml(data.review.reviewer_name)}</span>
                                            <span class="text-muted small">📍 ${escapeHtml(data.review.city)}</span>
                                        </div>
                                    </div>
                                `;
                                reviewsFeed.prepend(newReviewCard);
                            }

                            // Reset form fields
                            reviewForm.reset();
                            currentRating = 5;
                            ratingInput.value = 5;
                            updateStarsVisual(5, false);
                        } else {
                            if (alertBox) {
                                alertBox.innerHTML = `
                                    <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                        <strong>Error:</strong> Please check your inputs and try again.
                                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                    </div>
                                `;
                            }
                        }
                    })
                    .catch(err => {
                        console.error('Submission error:', err);
                        if (alertBox) {
                            alertBox.innerHTML = `
                                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                                    <strong>Network Error:</strong> Could not submit review. Please try again.
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                                </div>
                            `;
                        }
                    })
                    .finally(() => {
                        if (submitBtn) {
                            submitBtn.disabled = false;
                            submitBtn.innerHTML = originalBtnText;
                        }
                    });
            });
        }
    }

    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initReviewWidget);
    } else {
        initReviewWidget();
    }
})();
