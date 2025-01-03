# WildWestDiner - Interactive Menu System

## Overview
WildWestDiner's Interactive Menu System is a web-based restaurant ordering platform that allows customers to browse menu items, add them to cart, and complete payments through multiple payment methods. The system features a responsive design that works across desktop and mobile devices.

## Features
- **Interactive Menu Interface**
  - Categorized menu sections (Mains, Appetizers, Desserts)
  - Visual presentation of dishes with images, descriptions, and prices
  - Easy-to-use "Add to Cart" functionality

- **Shopping Cart**
  - Real-time cart updates
  - Quantity adjustment for items
  - Running total calculation
  - Item removal capability

- **Multiple Payment Options**
  - Credit/Debit Card processing
  - QR Code payment support
  - Alipay integration
  - PayNow support

## Technical Stack
- HTML5
- CSS3 with CSS Variables
- Vanilla JavaScript
- External Libraries:
  - QRCode.js for QR code generation
  - Google Fonts (Roboto)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd wildwestdiner-menu
```

2. Set up the development environment:
- No build tools required
- Simply open `index.html` in a web browser
- For local development, use a local server (e.g., Live Server for VS Code)

## Project Structure
```
wildwestdiner-menu/
├── index.html          # Main HTML file
├── images/            
│   ├── landing-page.png
│   ├── menu.png
│   ├── alipay-image.jpg
│   └── paynow-image.jpg
└── README.md
```

## Configuration
The menu items and prices can be configured in the `menuItems` object within the JavaScript code:

```javascript
const menuItems = {
    mains: [
        {
            name: 'Dish Name',
            description: 'Dish Description',
            price: 00.00,
            image: 'image-path'
        },
        // Add more items...
    ],
    // Add more categories...
};
```

## Payment System Integration

### Credit Card Processing
- Includes validation for card details
- Test card details are provided in the codebase
- Production implementation requires secure payment gateway integration

### QR Code Payments
- Generates dynamic QR codes based on cart total
- Supports multiple QR-based payment systems
- Integrates with local payment methods (PayNow, Alipay)

## Responsive Design
The system is responsive across different screen sizes:
- Desktop: Two-column layout (80/20 split)
- Tablet: Adjusted grid layout
- Mobile: Single column with floating cart

## Browser Support
- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Security Considerations
- Credit card information is validated but not stored
- Payment processing should be implemented through secure payment gateways
- HTTPS required for production deployment
- Input validation implemented for all user inputs

## Development Guidelines

### CSS Naming Conventions
- BEM methodology for class naming
- CSS variables for consistent theming
- Mobile-first approach for media queries

### JavaScript Best Practices
- Event delegation for dynamic elements
- Modular function organization
- Clear error handling

## Future Enhancements
1. Backend integration for order processing
2. User authentication system
3. Order history tracking
4. Kitchen display system integration
5. Real-time order status updates
6. Analytics dashboard
7. Inventory management integration
8. Customer loyalty program

## Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Support
For support or questions, please contact [support@wildwestdiner.com](mailto:support@wildwestdiner.com)

## Acknowledgments
- Design inspiration from modern restaurant ordering systems
- Icons and images from [appropriate credits]
- Community feedback and contributions

---
© 2025 WildWestDiner. All Rights Reserved.
