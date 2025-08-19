CREATE TABLE users_management (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    dob DATE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE project_management (
    id SERIAL PRIMARY KEY,
    project_unique_id VARCHAR(100) UNIQUE NOT NULL,
    project_name VARCHAR(255) NOT NULL,
    user VARCHAR(150),
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_project_user FOREIGN KEY (user) REFERENCES users_management(username) ON DELETE CASCADE
);

CREATE TABLE task_management (
    id SERIAL PRIMARY KEY,
    task_unique_id VARCHAR(100) UNIQUE NOT NULL,
    task_username VARCHAR(150) NOT NULL,
    task_name VARCHAR(255) NOT NULL,
    task_completion_date VARCHAR(100),
    task_status VARCHAR(20) DEFAULT 'pending',
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_task_user FOREIGN KEY (task_username) REFERENCES users_management(username) ON DELETE CASCADE
);

CREATE TABLE task_project_mapping (
    id SERIAL PRIMARY KEY,
    unique_id VARCHAR(100) UNIQUE NOT NULL,
    task_unique_id VARCHAR(100) NOT NULL,
    project_unique_id VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_mapping_task FOREIGN KEY (task_unique_id) REFERENCES task_management(task_unique_id) ON DELETE CASCADE,
    CONSTRAINT fk_mapping_project FOREIGN KEY (project_unique_id) REFERENCES project_management(project_unique_id) ON DELETE CASCADE
);

ALTER TABLE users_management
ADD COLUMN password VARCHAR(300);


INSERT INTO users_management (username, first_name, last_name, email, phone_number, dob)
VALUES ('johndoe', 'John', 'Doe', 'john@example.com', '9876543210', '1990-01-15');

INSERT INTO project_management (project_unique_id, project_name, username)
VALUES ('proj_001', 'Django CRM Project', 'johndoe');

INSERT INTO task_management (task_unique_id, task_username, task_name, task_completion_date, task_status)
VALUES ('task_001', 'johndoe', 'Design Models', '2025-08-10', 'in-progress');

INSERT INTO task_project_mapping (unique_id, task_unique_id, project_unique_id)
VALUES ('map_001', 'task_001', 'proj_001');

select * from users_management;

