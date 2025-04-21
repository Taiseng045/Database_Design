INSERT IGNORE INTO users (name, username, password, role, status, description, delete_at, created_at, updated_at)
VALUES 
    ('Admin', 'Admin@gmail.com', 
     'scrypt:32768:8:1$SmMFxvkm1AdzactS$1093e9462077e6a7a6b50064735879c0ab9a2937ca950130f97adc38229967fa8bb245a1630c1b8452708b3d1dc0a4d4cb4125d6ff8200048549610d0c5f5ea4', 
     'Admin', 'Active', 'Updated admin user', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('John Doe', 'john.doe@example.com', 
     'scrypt:32768:8:1$SmMFxvkm1AdzactS$1093e9462077e6a7a6b50064735879c0ab9a2937ca950130f97adc38229967fa8bb245a1630c1b8452708b3d1dc0a4d4cb4125d6ff8200048549610d0c5f5ea4', 
     'Officer', 'Active', 'Regular officer user', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Jane Smith', 'jane.smith@example.com', 
     'scrypt:32768:8:1$SmMFxvkm1AdzactS$1093e9462077e6a7a6b50064735879c0ab9a2937ca950130f97adc38229967fa8bb245a1630c1b8452708b3d1dc0a4d4cb4125d6ff8200048549610d0c5f5ea4', 
     'Director', 'Active', 'Director level user', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('Mike Johnson', 'mike.johnson@example.com', 
     'scrypt:32768:8:1$SmMFxvkm1AdzactS$1093e9462077e6a7a6b50064735879c0ab9a2937ca950130f97adc38229967fa8bb245a1630c1b8452708b3d1dc0a4d4cb4125d6ff8200048549610d0c5f5ea4', 
     'Guest', 'Active', 'Guest level user', NULL, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
