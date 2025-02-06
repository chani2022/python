from PyQt5.QtWidgets import QMessageBox

class MessageBox:

    @staticmethod
    def show(type, message):
        reply = None
        match type:
           case 'critical':
             reply = QMessageBox.critical(None, "Erreur", message, QMessageBox.Ok)
           case 'information':
              reply = QMessageBox.information(None, "Information", message, QMessageBox.Ok)
           case 'question':
              reply = QMessageBox.question(
                None,
                "Question",
                message,
                QMessageBox.Ok | QMessageBox.No,
                QMessageBox.No
            )
        return reply
        pass